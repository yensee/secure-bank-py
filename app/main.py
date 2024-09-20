from fastapi import FastAPI
from pydantic import BaseModel

from app.api.v1.endpoints import accounts, account_transfer, users
from app.api.v1.endpoints import admin
from app.db.session import engine
from app.models import account

# Base.metadata.create_all(bind=engine)

app = FastAPI()

# Initialize the database
account.Base.metadata.create_all(bind=engine)

# Include account-related routes
app.include_router(accounts.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1")
app.include_router(account_transfer.router,prefix="/api/v1")


# Transaction data model for fraud check
class TransactionData(BaseModel):
    sender_account_id: int
    receiver_account_id: int
    amount: float
    currency: str

# Simple fraud detection rule
def is_fraudulent(transaction: TransactionData):
    # Example rule: Any transaction over $10,000 is flagged as fraud
    if transaction.amount > 10000:
        return True
    # You can add more rules here for fraud detection
    return False

# Fraud check endpoint
@app.post("/check")
def check_fraud(transaction: TransactionData):
    fraud = is_fraudulent(transaction)
    return {"fraud": fraud}