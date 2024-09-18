from sqlalchemy.orm import Session
from app.models.account import Account
from app.schemas.account import AccountCreate

def create_account(db: Session, account: AccountCreate):
    db_account = Account(
        account_number=account.account_number,
        balance=account.balance,
        customer_name=account.customer_name
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_account_by_id(db: Session, account_id: int):
    return db.query(Account).filter(Account.id == account_id).first()
