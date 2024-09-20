from pydantic import BaseModel

class AccountBase(BaseModel):
    account_number: str
    balance: float
    customer_name: str
    currency: str  # Add this field to represent account currency
    account_status: str

class AccountCreate(AccountBase):
    pass

class AccountRead(AccountBase):
    id: int

    class Config:
        orm_mode = True
