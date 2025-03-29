from fastapi import APIRouter, Depends, HTTPException
from utils.jwt import verify_token
from fastapi.security import OAuth2PasswordBearer
from database.db import db
from bson import ObjectId

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Saha çalışması oluşturma
@router.post("/saha-calismasi")
def create_saha_calismasi(data: dict, token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")

        data["created_by"] = email
        data["status"] = "devam ediyor"
        db["saha_calismalari"].insert_one(data)
        return {"message": "Saha çalışması başarıyla oluşturuldu."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Kendi saha çalışmalarını listeleme
@router.get("/saha-calismalarim")
def get_saha_calismalari(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")

        calismalar = db["saha_calismalari"].find({"created_by": email})
        result = []
        for c in calismalar:
            c["_id"] = str(c["_id"])
            result.append(c)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Belirli bir saha çalışmasını güncelleme
@router.put("/saha-calismasi/{id}")
def update_saha_calismasi(id: str, updated_data: dict, token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")

        result = db["saha_calismalari"].update_one(
            {"_id": ObjectId(id), "created_by": email},
            {"$set": updated_data}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Saha çalışması bulunamadı veya güncellenemedi.")

        return {"message": "Saha çalışması güncellendi."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Belirli bir saha çalışmasını silme
@router.delete("/saha-calismasi/{id}")
def delete_saha_calismasi(id: str, token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token)
        email = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Kullanıcı doğrulanamadı")

        result = db["saha_calismalari"].delete_one({"_id": ObjectId(id), "created_by": email})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Saha çalışması bulunamadı veya silinemedi.")

        return {"message": "Saha çalışması silindi."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
