from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db
from ..auth import get_current_user_id

router = APIRouter()

@router.post("/", response_model=schemas.Transaction)
def create_new_transaction(
    transaction: schemas.TransactionCreate, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id) 
):
    """
    Create a new transaction for a given account, but only if the logged-in
    user is the owner of the account.
    """
    # --- AUTHORIZATION LOGIC START ---
    
    # 1. Get the target account from the database
    db_account = crud.get_account_by_id(db, account_id=transaction.account_id)

    # 2. First, check if the account exists
    if not db_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    # 3. Check if the logged-in user (from token) is the owner of the account
    if db_account.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform transactions on this account."
        )

    # --- AUTHORIZATION LOGIC END ---
    
    # If authorization passes, proceed to create the transaction
    # The validation for account status is still inside create_transaction
    return crud.create_transaction(db=db, transaction=transaction)


@router.get("/{account_id}", response_model=List[schemas.Transaction])
def read_transactions_for_account(
    account_id: int, 
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    """
    Retrieve transactions, but only if the user owns the account.
    """
    # --- AUTHORIZATION LOGIC START ---
    db_account = crud.get_account_by_id(db, account_id=account_id)

    if not db_account:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

    if db_account.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to view these transactions."
        )
    # --- AUTHORIZATION LOGIC END ---
    
    return crud.get_transactions_by_account(db, account_id=account_id)

