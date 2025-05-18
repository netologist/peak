from fastapi import Request, Depends
from fastapi.templating import Jinja2Templates
from .base_controller import BaseController
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.utils.database import get_db
from sqlalchemy.orm import Session

templates = Jinja2Templates(directory="app/templates")

class ViewController(BaseController):
    def __init__(self):
        super().__init__()
        self.setup_routes()

    def setup_routes(self):
        self.router.get("/", tags=["views"])(self.index)
        self.router.get("/users", tags=["views"])(self.users_page)

    async def index(self, request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    async def users_page(self, request: Request, db: Session = Depends(get_db)):
        repo = UserRepository(db)
        service = UserService(repo)
        users = service.get_all_users()
        return templates.TemplateResponse("users.html", {"request": request, "users": users})