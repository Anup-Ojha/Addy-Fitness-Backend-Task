from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from models.user import User
from schemas.user import UserInDB
from app.core.security import verify_token   

router = APIRouter(
    tags=["users"],
    dependencies=[Depends(verify_token)]  
)


# Get all active users with pagination
@router.get("/", response_model=List[UserInDB])
def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=10),
    db: Session = Depends(get_db)
):
    return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

# Get a specific user by ID
@router.get("/{user_id}", response_model=UserInDB)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update a specific user
@router.put("/{user_id}", response_model=UserInDB)
def update_user(user_id: int, updated_user: UserInDB, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.full_name = updated_user.full_name
    user.phone = updated_user.phone
    db.commit()
    db.refresh(user)
    return user

# Soft delete a user (deactivate)
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.is_active = False
    db.commit()
    return {"message": f"User {user.email} deactivated successfully"}
