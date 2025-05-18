from fastapi import APIRouter, Depends
from app.config.settings import get_settings

class BaseController:
    def __init__(self):
        self.settings = get_settings()
        self.router = APIRouter()