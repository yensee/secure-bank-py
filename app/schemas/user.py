from typing import Optional

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    # username: str | None = None (New style > 3.9.6 version)
    username: Optional[str] = None
    role:Optional[str] = None
