from crud import *

from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from pydantic import BaseModel, EmailStr, SecretStr

from typing import Optional

app = FastAPI()

@app.post("/account", tags=['user'], status_code=201)
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



