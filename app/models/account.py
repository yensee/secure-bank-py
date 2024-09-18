from sqlalchemy import Column, Integer, String, Float
from app.db.session import Base
from sqlalchemy.orm import relationship

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String(16), unique=True, index=True, nullable=False)
    balance = Column(Float, nullable=False)
    customer_name = Column(String(20), nullable=False)
    account_status = Column(String(10), default="ACTIVE")


    # Establish a one-to-many relationship with the Transaction model
    transactions = relationship("Transaction", back_populates="account")