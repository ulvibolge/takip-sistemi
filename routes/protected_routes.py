from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from utils.jwt import verify_token
from database.db import db
from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class UserResponse(BaseModel):
    id: str
    email: str

@router.get("/protected", response_model=UserResponse)
def get_my_profile(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        user_id = ObjectId(payload["sub"])
    except InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Geçersiz kullanıcı ID formatı"
        )

    user = db["users"].find_one({"_id": user_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Kullanıcı bulunamadı"
        )

    return UserResponse(
        id=str(user["_id"]),
        email=user["email"]
    )