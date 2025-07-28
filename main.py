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

@app.post("/users")
async def create_user_endpoint(user: User) -> User:
    return await create_user(user)

@app.post("/login")
async def login_access(l: Login) -> dict:
    return await login(l)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")