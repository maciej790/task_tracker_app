from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from databse.config import get_session
from services.auth import login_user, create_access_token, get_current_user
from services.exception import create_exception
from models.user import User

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

# Login endpoint
@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    user = login_user(form_data.username, form_data.password, db)
    if not user:
        create_exception("Invalid username or password", 401)

    access_token = create_access_token(user.id, user.username)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

# Get logged user info
@router.get("/logged", response_model=User)
async def get_logged_user(user: User = Depends(get_current_user)):
    return user
