from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

from app.config.settings import get_settings
from app.middleware.middleware_handler import setup_middlewares
from app.controllers.user_controller import UserController
from app.utils.database import create_db_and_tables

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG
)

# Setup middleware
setup_middlewares(app)

# Setup static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup controllers
app.include_router(UserController().router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()

# Templates setup
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI Laravel-like structure!"}