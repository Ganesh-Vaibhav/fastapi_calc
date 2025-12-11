from typing import Generator, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import models, schemas, security
from .dependencies import get_db


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
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


@router.post("/login", response_model=schemas.Token)
def login(
    credentials: schemas.LoginRequest,
    db: Session = Depends(get_db),
):
    if not credentials.username and not credentials.email:
        raise HTTPException(status_code=400, detail="Username or email is required")

    query = db.query(models.User)
    if credentials.username:
        query = query.filter(models.User.username == credentials.username)
    if credentials.email:
        query = query.filter(models.User.email == credentials.email)

    user = query.first()
    if not user or not security.verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = security.timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/me", response_model=schemas.UserRead)
def update_user_me(
    user_update: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    if user_update.username:
        # Check if username already exists
        existing_user = db.query(models.User).filter(models.User.username == user_update.username).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Username already taken")
        current_user.username = user_update.username
    
    if user_update.email:
        # Check if email already exists
        existing_user = db.query(models.User).filter(models.User.email == user_update.email).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=400, detail="Email already taken")
        current_user.email = user_update.email

    try:
        db.commit()
        db.refresh(current_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    return current_user


@router.post("/me/password", status_code=status.HTTP_200_OK)
def change_password(
    password_change: schemas.PasswordChange,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_user),
):
    if not security.verify_password(password_change.old_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect old password")
    
    if password_change.old_password == password_change.new_password:
        raise HTTPException(status_code=400, detail="New password cannot be the same as old password")

    current_user.password_hash = security.hash_password(password_change.new_password)
    db.commit()
    
    return {"message": "Password updated successfully"}
