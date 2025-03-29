from fastapi import FastAPI
from routes.auth_routes import router as auth_router
from routes.protected_routes import router as protected_router
from routes.profile_routes import router as profile_router
from routes.saha_routes import router as saha_router
from database.db import db  # opsiyonel ama bağlantıyı test etmek istersen kullanılır

app = FastAPI()

# Rotaları bağla
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(protected_router, prefix="/auth", tags=["Protected"])
app.include_router(profile_router, tags=["Profile"])
app.include_router(saha_router, tags=["Saha Çalışması"])


@app.get("/")
def read_root():
    return {"message": "Takip Sistemi API çalışıyor."}

@app.get("/ping-mongo")
def ping_mongo():
    try:
        db.command("ping")
        return {"status": "success", "message": "MongoDB bağlantısı başarılı!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
