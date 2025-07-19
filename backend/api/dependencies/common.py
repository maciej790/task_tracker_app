from fastapi import Depends
from sqlmodel import Session
from services.auth import get_current_user
from databse.config import get_session
from models.user import User

def get_user_and_db(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    return user, db
