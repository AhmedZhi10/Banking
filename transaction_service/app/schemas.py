from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

# --- Transaction Schemas ---

# This is the "base" schema with fields common to creating and reading.
class TransactionBase(BaseModel):
    amount: Decimal
    account_id: int

# Schema for creating a new transaction (what the user sends us).
# It inherits from the base schema.
class TransactionCreate(TransactionBase):
    pass # No extra fields needed for creation

# Schema for reading a transaction (what we send back to the user).
class Transaction(TransactionBase):
    id: int
    transaction_date: datetime

    # This tells Pydantic to read the data even if it is not a dict,
    # but an ORM model (or any other arbitrary object with attributes).
    class Config:
        from_attributes = True