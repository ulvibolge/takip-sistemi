from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from utils.jwt import verify_token
from database.db import db
from bson import ObjectId

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/me")
def get_my_profile(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    user_id = payload["sub"]  # JWT içinde sakladığımız kullanıcı ID

    user = db["users"].find_one({"_id": ObjectId(user_id)})

    if not user:
        return {"message": "Kullanıcı bulunamadı."}

    return {
        "id": str(user["_id"]),
        "email": user["email"]
    }
@router.get("/me")
def get_my_profile(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        print("Payload:", payload)  # LOG

        user_id = ObjectId(payload["sub"])
        print("User ID:", user_id)  # LOG

        user = db["users"].find_one({"_id": user_id})
        print("User found:", user)  # LOG

        if not user:
            return {"error": "Kullanıcı bulunamadı."}

        return {
            "id": str(user["_id"]),
            "email": user["email"]
        }

    except Exception as e:
        print("Hata:", str(e))
        return {"error": f"Bir hata oluştu: {str(e)}"}

