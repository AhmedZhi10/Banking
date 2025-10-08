from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .database import Base

class Account(Base):
    __tablename__ = "account_account"

    id = Column(Integer, primary_key=True)
    status_id = Column(Integer)
    user_id = Column(Integer)
    # --- ADD THIS LINE ---
    # This allows us to read and write to the balance column.
    balance = Column(Numeric(15, 2), nullable=False)
    
    transactions = relationship("Transaction", back_populates="account")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    account_id = Column(Integer, ForeignKey("account_account.id"), nullable=False)

    account = relationship("Account", back_populates="transactions")

