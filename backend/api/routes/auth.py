from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from databse.config import get_session
from services.auth import login_user, create_access_token
from services.auth import get_current_user
from services.exception import create_exception

router = APIRouter()

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_session)
):
    user = login_user(form_data.username, form_data.password, db)
    if not user:
        create_exception("Invalid username or password", 401)
    access_token = create_access_token(user.id, user.username)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/logged')
async def getLoggedUser(user = Depends(get_current_user)):
    return user