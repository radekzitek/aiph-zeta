from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import User, UserCreate, UserUpdate
from app.crud import user as crud_user
from app.db.database import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    logger.debug(f"POST /api/v1/users/ - Creating user with data: {user_in.dict()}")
    user = crud_user.create_user(db, user_in)
    logger.debug(f"POST /api/v1/users/ - Created user: {user}")
    return user


@router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logger.debug(f"GET /api/v1/users/ - Fetching users with skip={skip}, limit={limit}")
    users = crud_user.get_users(db, skip=skip, limit=limit)
    logger.debug(f"GET /api/v1/users/ - Fetched users: {users}")
    return users


@router.get("/{user_id}", response_model=User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    logger.debug(f"GET /api/v1/users/{user_id} - Fetching user")
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        logger.warning(f"GET /api/v1/users/{user_id} - User not found")
        raise HTTPException(status_code=404, detail="User not found")
    logger.debug(f"GET /api/v1/users/{user_id} - Fetched user: {db_user}")
    return db_user


@router.put("/{user_id}", response_model=User)
def update_user(user_id: str, user_in: UserUpdate, db: Session = Depends(get_db)):
    logger.debug(
        f"PUT /api/v1/users/{user_id} - Updating user with data: {user_in.dict(exclude_unset=True)}"
    )
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        logger.warning(f"PUT /api/v1/users/{user_id} - User not found")
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = crud_user.update_user(db, db_user, user_in)
    logger.debug(f"PUT /api/v1/users/{user_id} - Updated user: {updated_user}")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    logger.debug(f"DELETE /api/v1/users/{user_id} - Deleting user")
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        logger.warning(f"DELETE /api/v1/users/{user_id} - User not found")
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.delete_user(db, db_user)
    logger.debug(f"DELETE /api/v1/users/{user_id} - User deleted successfully")
