from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    account_id: int
    transaction_type: str
    amount: float

class TransactionRead(BaseModel):
    id: int
    transaction_type: str
    amount: float
    timestamp: datetime

    class Config:
        orm_mode = True

