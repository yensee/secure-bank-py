from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.user import get_admin_users
from app.db.session import SessionLocal
from app.crud.transaction import count_transactions
from app.core.security import get_current_user
from app.schemas.user import TokenData
from app.schemas.user import UserRead, TokenData

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to get system metrics (e.g., total number of transactions)
@router.get("/admin/metrics")
def get_system_metrics(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # Ensure that only admins can access this route
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")

    transaction_count = count_transactions(db)
    return {
        "transactions_processed": transaction_count
    }

# Endpoint to list all system administrators
@router.get("/admin/users", response_model=list[UserRead])
def list_admin_users(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # Ensure that only admins can access this route
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Not authorized")

    return get_admin_users(db)
