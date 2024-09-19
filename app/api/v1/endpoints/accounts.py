from app.schemas.account import AccountCreate, AccountRead
from app.crud.account import create_account, get_account_by_id
from app.crud.transaction import get_transactions_by_account_id
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.transaction import TransactionCreate, TransactionRead
from app.crud.transaction import create_transaction
from app.db.session import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from app.core.security import get_current_user
from app.schemas.user import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

# Dependency to get DB sessio
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create a new account
@router.post("/accounts/", response_model=AccountRead)
def create_new_account(account: AccountCreate,
                       db: Session = Depends(get_db)
                       ):
    return create_account(db=db, account=account)

# Endpoint to get account details by ID
@router.get("/accounts/{account_id}", response_model=AccountRead)
def read_account(account_id: int, db: Session = Depends(get_db),current_user: TokenData = Depends(get_current_user)):
    db_account = get_account_by_id(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

# Endpoint to get transactions for an account by account ID
@router.get("/accounts/{account_id}/transactions", response_model=list[TransactionRead])
def get_account_transactions(account_id: int, db: Session = Depends(get_db),current_user: TokenData = Depends(get_current_user)):
    db_account = get_account_by_id(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    transactions = get_transactions_by_account_id(db, account_id)
    return transactions

# Endpoint to post a new transaction
@router.post("/accounts/{account_id}/transactions", response_model=TransactionRead)
def post_transaction(account_id: int, transaction: TransactionCreate, db: Session = Depends(get_db)):
    # Ensure that the account ID in the URL matches the one in the request body
    if account_id != transaction.account_id:
        raise HTTPException(status_code=400, detail="Account ID mismatch")

    return create_transaction(db=db, transaction=transaction)