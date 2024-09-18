from sqlalchemy.orm import Session
from app.models.transaction import Transaction

def get_transactions_by_account_id(db: Session, account_id: int):
    return db.query(Transaction).filter(Transaction.account_id == account_id).all()


from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.account import Account
from app.schemas.transaction import TransactionCreate
from fastapi import HTTPException

def create_transaction(db: Session, transaction: TransactionCreate):
    # Find the account by ID
    account = db.query(Account).filter(Account.id == transaction.account_id).first()

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Adjust account balance based on the transaction type
    if transaction.transaction_type == 'DEPOSIT':
        account.balance += transaction.amount
    elif transaction.transaction_type == 'WITHDRAWAL':
        if account.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        account.balance -= transaction.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    # Create the transaction
    db_transaction = Transaction(
        account_id=transaction.account_id,
        transaction_type=transaction.transaction_type,
        amount=transaction.amount
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    db.refresh(account)  # Update the account balance in the database

    return db_transaction
