from backend.db.crud import *

from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr, SecretStr

from typing import Optional

router = APIRouter()

@router.post("/account", tags=["Authentication"], status_code=201)
async def register_user(
    email: EmailStr = Form(...),
    username: str = Form(...),
    password: SecretStr = Form(...),
    photo: Optional[UploadFile] = Form(None)):

    user = {"email": email, "username": username}

    if check_email(email):
        raise HTTPException(status_code=409, detail="Email already registered")

    if check_username(username):
        raise HTTPException(status_code=409, detail="Username already taken")

    password_ = password.get_secret_value()

    if not create_user(email, username, password_):
        raise HTTPException(status_code=500, detail="Internal server error")

    return user

@router.post("/session", tags=["Authentication"], status_code=200)
async def autenticate_user(
    username: str = Form(...),
    password: SecretStr = Form(...)):

    password_ = password.get_secret_value()

    user = get_user(username, password_)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    user['token'] = 145

    user = {k.lower(): v for k, v in user.items()}

    return user
  
