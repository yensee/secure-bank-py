from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserRead, Token
from app.crud.user import create_user, get_user_by_username, get_all_users
from app.db.session import SessionLocal
from app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, create_refresh_token, \
    REFRESH_TOKEN_EXPIRE_MINUTES, verify_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordBearer
from app.core.security import get_current_user
from app.schemas.user import TokenData


router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Register a new user
@router.post("/register/", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)

# Login and generate both access and refresh tokens
@router.post("/login/", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(data={"sub": user.username,"role": user.role}, expires_delta=access_token_expires)
    refresh_token = create_refresh_token(data={"sub": user.username,"role": user.role}, expires_delta=refresh_token_expires)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# Refresh token endpoint to generate a new access token
@router.post("/refresh-token/", response_model=Token)
def refresh_access_token(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the refresh token
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception

    # Generate a new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": token_data.username}, expires_delta=access_token_expires)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Get a list of all users
@router.get("/users/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db),current_user: TokenData = Depends(get_current_user)):
    users = get_all_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="No users found")
    return users