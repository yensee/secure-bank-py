from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AccountTransferCreate(BaseModel):
    sender_account_id: int
    receiver_account_id: int
    amount: float
    currency: str  # Currency of the sender

class AccountTransferRead(BaseModel):
    id: int
    sender_account_id: int
    receiver_account_id: int
    amount: float
    currency: str
    exchange_rate: Optional[float]
    converted_amount: Optional[float]
    status: str
    timestamp: datetime

    class Config:
        orm_mode = True
