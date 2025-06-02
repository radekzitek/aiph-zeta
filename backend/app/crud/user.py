from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import Optional, List
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy import select
import uuid
import logging

logger = logging.getLogger("__name__")


def get_user(db: Session, user_id: str) -> Optional[User]:
    logger.debug(f"Fetching user by id: {user_id}")
    user = db.get(User, user_id)
    logger.debug(f"Fetched user: {user}")
    return user


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    logger.debug(f"Fetching user by username: {username}")
    stmt = select(User).where(User.username == username)
    user = db.execute(stmt).scalar_one_or_none()
    logger.debug(f"Fetched user: {user}")
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    logger.debug(f"Fetching user by email: {email}")
    stmt = select(User).where(User.email == email)
    user = db.execute(stmt).scalar_one_or_none()
    logger.debug(f"Fetched user: {user}")
    return user


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    logger.debug(f"Fetching users with skip={skip}, limit={limit}")
    stmt = select(User).offset(skip).limit(limit)
    users = db.execute(stmt).scalars().all()
    logger.debug(f"Fetched users: {users}")
    return users


def create_user(
    db: Session, user_in: UserCreate, created_by: Optional[str] = None
) -> User:
    logger.debug(f"Creating user: {user_in.dict()}")
    db_user = User(
        id=str(uuid.uuid4()),
        username=user_in.username,
        email=user_in.email,
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        hashed_password=user_in.password,  # Hash in real app!
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
        created_by=created_by,
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        logger.debug(f"User created successfully: {db_user}")
    except IntegrityError as e:
        db.rollback()
        logger.error(f"IntegrityError while creating user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists."
        )
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error while creating user: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error.",
        )
    return db_user


def update_user(
    db: Session, db_user: User, user_in: UserUpdate, updated_by: Optional[str] = None
) -> User:
    logger.debug(
        f"Updating user {db_user.id} with data: {user_in.dict(exclude_unset=True)}"
    )
    for field, value in user_in.dict(exclude_unset=True).items():
        setattr(db_user, field, value)
    if updated_by:
        db_user.updated_by = updated_by
    try:
        db.commit()
        db.refresh(db_user)
        logger.debug(f"User updated successfully: {db_user}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating user {db_user.id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error.",
        )
    return db_user


def delete_user(db: Session, db_user: User) -> None:
    logger.debug(f"Deleting user: {db_user.id}")
    try:
        db.delete(db_user)
        db.commit()
        logger.debug(f"User deleted successfully: {db_user.id}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting user {db_user.id}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error.",
        )
