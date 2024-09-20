from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.session import Base
from datetime import datetime

class AccountTransfer(Base):
    __tablename__ = "account_transfers"

    id = Column(Integer, primary_key=True, index=True)
    sender_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    receiver_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False)  # e.g., "USD", "EUR"
    exchange_rate = Column(Float, nullable=True)  # Only used for currency conversion
    converted_amount = Column(Float, nullable=True)  # Amount after conversion
    status = Column(String(20), default="PENDING")  # PENDING, COMPLETED, FAILED
    timestamp = Column(DateTime, default=datetime.utcnow)

    sender_account = relationship("Account", foreign_keys=[sender_account_id])
    receiver_account = relationship("Account", foreign_keys=[receiver_account_id])
