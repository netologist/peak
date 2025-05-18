from typing import Dict, List, Optional, Type, TypeVar, Generic
from sqlalchemy.orm import Session
from app.models.base import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_all(self) -> List[T]:
        return self.db.query(self.model).all()

    def get_by_id(self, id: int) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def create(self, data: Dict) -> T:
        db_item = self.model(**data)
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, id: int, data: Dict) -> Optional[T]:
        db_item = self.get_by_id(id)
        if db_item:
            for key, value in data.items():
                setattr(db_item, key, value)
            self.db.commit()
            self.db.refresh(db_item)
        return db_item

    def delete(self, id: int) -> bool:
        db_item = self.get_by_id(id)
        if db_item:
            self.db.delete(db_item)
            self.db.commit()
            return True
        return False