from sqlalchemy.orm import Session
from app.models.account_transfer import AccountTransfer
from app.schemas.account_transfer import AccountTransferCreate

def create_account_transfer(db: Session, transfer: AccountTransferCreate, converted_amount: float = None, exchange_rate: float = None):
    db_transfer = AccountTransfer(
        sender_account_id=transfer.sender_account_id,
        receiver_account_id=transfer.receiver_account_id,
        amount=transfer.amount,
        currency=transfer.currency,
        converted_amount=converted_amount,
        exchange_rate=exchange_rate,
        status="PENDING"
    )
    db.add(db_transfer)
    db.commit()
    db.refresh(db_transfer)
    return db_transfer

def update_account_transfer_status(db: Session, transfer_id: int, status: str):
    transfer = db.query(AccountTransfer).filter(AccountTransfer.id == transfer_id).first()
    if transfer:
        transfer.status = status
        db.commit()
        db.refresh(transfer)
    return transfer

def get_account_transfer_by_id(db: Session, transfer_id: int):
    return db.query(AccountTransfer).filter(AccountTransfer.id == transfer_id).first()
