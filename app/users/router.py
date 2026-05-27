from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import bcrypt

from app.database import get_db
from app.users.models import User
from app.users.schemas import UserCreate, UserOut, UserUpdate
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["User Management"])


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Register a new user. Passwords are hashed with bcrypt before storage.",
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{payload.username}' is already taken.",
        )

    # Hash the password before storing — NEVER store plain text
    hashed = bcrypt.hashpw(payload.password.encode("utf-8"), bcrypt.gensalt())

    new_user = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hashed.decode("utf-8"),
        role=payload.role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get my profile",
    description="Returns the profile of the currently authenticated user. **Requires JWT token.**",
)
def get_my_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.get(
    "/",
    response_model=List[UserOut],
    summary="List all users (Admin only)",
    description="Returns all users in the system. **Requires JWT token with admin role.**",
)
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can view all users.",
        )
    return db.query(User).all()


@router.get(
    "/{user_id}",
    response_model=UserOut,
    summary="Get user by ID",
    description="Fetch a specific user by their ID. **Requires JWT token.**",
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id={user_id} not found.",
        )
    return user


@router.patch(
    "/{user_id}",
    response_model=UserOut,
    summary="Update a user",
    description="Update user details. **Requires JWT token.**",
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user (Admin only)",
    description="Permanently deletes a user. **Admin role required.**",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admins can delete users.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    db.delete(user)
    db.commit()
