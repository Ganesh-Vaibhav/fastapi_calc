from typing import Generator, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas, security
from .db import SessionLocal


router = APIRouter(prefix="/users", tags=["users"])


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = models.User(
        username=user_in.username,
        email=user_in.email,
        password_hash=security.hash_password(user_in.password),
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    db.refresh(user)
    return user


@router.post("/login")
def login(
    username: Optional[str] = None,
    email: Optional[str] = None,
    password: str = "",
    db: Session = Depends(get_db),
):
    if not username and not email:
        raise HTTPException(status_code=400, detail="Username or email is required")

    query = db.query(models.User)
    if username:
        query = query.filter(models.User.username == username)
    if email:
        query = query.filter(models.User.email == email)

    user = query.first()
    if not user or not security.verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"authenticated": True, "user": schemas.UserRead.model_validate(user)}
