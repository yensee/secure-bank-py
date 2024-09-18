from pydantic import BaseModel

class AccountCreate(BaseModel):
    account_number: str
    balance: float
    customer_name: str

class AccountRead(BaseModel):
    id: int
    account_number: str
    balance: float
    customer_name: str
    account_status: str

    class Config:
        orm_mode = True
