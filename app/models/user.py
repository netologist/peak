from sqlalchemy import Column, String, Boolean
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)