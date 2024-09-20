from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.account import get_account_by_id
from app.schemas.account_transfer import AccountTransferCreate, AccountTransferRead
from app.crud.account_transfer import create_account_transfer, update_account_transfer_status
from app.db.session import SessionLocal
from app.services.external_apis import check_fraud_detection, get_exchange_rate

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/account-transfers/", response_model=AccountTransferRead)
def create_new_account_transfer(transfer: AccountTransferCreate, db: Session = Depends(get_db)):
    # Step 1: Fraud detection
    if check_fraud_detection(transfer.dict()):
        raise HTTPException(status_code=400, detail="Transfer flagged as fraud")

    # Step 2: Currency exchange if sender and receiver have different currencies
    sender_account = get_account_by_id(db, transfer.sender_account_id)
    receiver_account = get_account_by_id(db, transfer.receiver_account_id)

    if sender_account.currency != receiver_account.currency:
        exchange_rate = get_exchange_rate(sender_account.currency, receiver_account.currency)
        if exchange_rate is None:
            raise HTTPException(status_code=503, detail="Currency conversion service unavailable")
        converted_amount = transfer.amount * exchange_rate
    else:
        exchange_rate = None
        converted_amount = transfer.amount

    # Step 3: Create the account transfer
    db_transfer = create_account_transfer(db, transfer, converted_amount=converted_amount, exchange_rate=exchange_rate)

    # Step 4: Update the transfer status after successful creation
    update_account_transfer_status(db, db_transfer.id, "COMPLETED")

    return db_transfer
