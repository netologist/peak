from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .base_controller import BaseController
from app.models.user import User
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.utils.database import get_db
from app.schemas.user import UserCreate, UserResponse

class UserController(BaseController):
    def __init__(self):
        super().__init__()
        self.setup_routes()

    def setup_routes(self):
        self.router.post("/users/", response_model=UserResponse, tags=["users"])(self.create_user)
        self.router.get("/users/", response_model=List[UserResponse], tags=["users"])(self.get_users)
        self.router.get("/users/{user_id}", response_model=UserResponse, tags=["users"])(self.get_user)

    async def create_user(self, user: UserCreate, db: Session = Depends(get_db)):
        repo = UserRepository(db)
        service = UserService(repo)
        return service.create_user(user)

    async def get_users(self, db: Session = Depends(get_db)):
        repo = UserRepository(db)
        service = UserService(repo)
        return service.get_all_users()

    async def get_user(self, user_id: int, db: Session = Depends(get_db)):
        repo = UserRepository(db)
        service = UserService(repo)
        user = service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user