from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database.db import db
from core.security import hash_password, verify_password, create_access_token
from schemas.user_schema import UserCreate, UserLogin
from datetime import datetime


router = APIRouter()



# Kullanıcı Kaydı
@router.post("/register", status_code=201)
def register(user: UserCreate):
    if db["users"].find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Bu e-posta zaten kayıtlı.")

    hashed_pw = hash_password(user.password)
    new_user = {
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_pw,
        "created_at": datetime.utcnow()
    }

    result = db["users"].insert_one(new_user)
    return {"message": "Kayıt başarılı", "user_id": str(result.inserted_id)}

# Kullanıcı Giriş
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db["users"].find_one({"email": form_data.username})  # username=email
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Geçersiz e-posta veya şifre")

    token_data = {
        "sub": str(user["_id"]),
        "email": user["email"]
    }

    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


from core.security import get_current_user
from fastapi import Depends


# Korumalı Alan
@router.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": f"Hoş geldin {current_user['email']}, bu korumalı bir alandır!"
    }