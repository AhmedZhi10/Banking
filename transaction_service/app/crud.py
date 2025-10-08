from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import models, schemas

# This helper function remains the same
def get_account_by_id(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

# This function remains the same
def get_transactions_by_account(db: Session, account_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).filter(models.Transaction.account_id == account_id).all()


# --- THIS IS THE UPDATED FUNCTION ---
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    """
    Creates a transaction, but first validates account status and balance.
    Then, it updates the account balance. All in one atomic operation.
    """
    account_to_update = get_account_by_id(db, account_id=transaction.account_id)

    # 1. Validation for account existence and status (already done)
    if not account_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Account {transaction.account_id} not found.")
    
    ACTIVE_STATUS_ID = 1
    if account_to_update.status_id != ACTIVE_STATUS_ID:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account is not active.")

    # --- NEW FINANCIAL LOGIC START ---

    # 2. Check for sufficient balance if it's a withdrawal (negative amount)
    is_withdrawal = transaction.amount < 0
    if is_withdrawal and account_to_update.balance < abs(transaction.amount):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds for this withdrawal."
        )

    # 3. Update the account balance
    # This single line works for both deposits (+) and withdrawals (-)
    account_to_update.balance += transaction.amount

    # --- NEW FINANCIAL LOGIC END ---

    # 4. Create the transaction record
    db_transaction = models.Transaction(**transaction.model_dump())
    
    # Add both the updated account and the new transaction to the session
    db.add(db_transaction)
    db.add(account_to_update)
    
    # 5. Commit everything as a single, atomic transaction
    # Either both succeed, or both fail. This ensures data consistency.
    db.commit()
    
    db.refresh(db_transaction)
    return db_transaction

