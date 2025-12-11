from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas import UserCreate, UserRead, UserLogin, Token, UserUpdate, PasswordChange
from app.security import hash_password, verify_password, create_access_token

router = APIRouter()

def get_current_user(db: Session, request: Request):
    """Extract user from JWT token in Authorization header."""
    from app.security import decode_access_token
    from jose import JWTError
    
    auth = request.headers.get("authorization")
    if not auth or not auth.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    
    token = auth.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Get current user info endpoint
@router.get("/users/me", response_model=UserRead)
def get_me(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(db, request)
    return user

# Profile update endpoint
@router.put("/users/profile", response_model=UserRead)
def update_profile(update: UserUpdate, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(db, request)
    if update.username:
        # Check for username uniqueness
        if db.query(User).filter(User.username == update.username, User.id != user.id).first():
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = update.username
    if update.email:
        if db.query(User).filter(User.email == update.email, User.id != user.id).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        user.email = update.email
    db.commit()
    db.refresh(user)
    return user

# Password change endpoint
@router.post("/users/change-password", status_code=status.HTTP_204_NO_CONTENT)
def change_password(payload: PasswordChange, request: Request, db: Session = Depends(get_db)):
    user = get_current_user(db, request)
    if not verify_password(payload.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="Old password incorrect")
    user.password_hash = hash_password(payload.new_password)
    db.commit()
    return

@router.post("/users", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check uniqueness
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



@router.post("/users/register", response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Alias for create_user that matches assignment `/users/register`."""
    return create_user(user, db)


@router.post("/users/login", response_model=Token)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    """Verify username/password and return a JWT access token."""
    user = db.query(User).filter(User.username == payload.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token)
