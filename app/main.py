from fastapi import FastAPI
from app.api.v1.endpoints import accounts
from app.models import account
from app.db.session import engine
from app.models.account import Base
from app.models.transaction import Transaction

# Base.metadata.create_all(bind=engine)

app = FastAPI()

# Initialize the database
account.Base.metadata.create_all(bind=engine)

# Include account-related routes
app.include_router(accounts.router, prefix="/api/v1")
