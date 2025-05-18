from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.password import hash_password

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreate):
        hashed_password = hash_password(user_data.password)
        return self.repository.create({
            "name": user_data.name,
            "email": user_data.email,
            "password": hashed_password
        })

    def get_all_users(self):
        return self.repository.get_all()

    def get_user_by_id(self, user_id: int):
        return self.repository.get_by_id(user_id)