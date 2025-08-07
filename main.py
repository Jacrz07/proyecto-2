import uvicorn
import logging
from controllers.users import create_user, login
from models.users import User
from fastapi import FastAPI, Request
from models.login import Login
from utils.security import validateuser, validateadmin

from routes.catalogs import router as catalogs_router
from routes.inventary import router as inventary_router

app = FastAPI()

app.include_router(catalogs_router)
app.include_router(inventary_router)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"message" : "wenas"}

@app.get("/health")
def health_check():
    try:
        return {
            "status" : "healthy",
            "timestamp" : "2025-08-06",
            "service" : "gamestore-api",
            "enviroment" : "production"
        }
    except Exception as e:
        return {"status" : "unhealthy", "error": str(e)}

@app.get("/ready")
def readliness_check():
    try:
        from utils.mongodb import test_connection
        db_status = test_connection()
        return {
            "status" : "ready" if db_status else "not_ready",
            "database" : "connected" if db_status else "disconnected",
            "service" : "gamestore-api"
        }
    except Exception as e:
        return {"status" : "not_ready"}

@app.post("/users")
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

@app.post("/login")
async def login_access(l: Login) -> dict:
    return await login(l)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")