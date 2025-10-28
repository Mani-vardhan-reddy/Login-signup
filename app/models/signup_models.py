from app.database.database import Base
from sqlalchemy import Column, String, VARCHAR, INTEGER, Boolean, TEXT, DateTime, String
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
import uuid
from typing import Type, List, Optional
from app.database.database import SessionLocal

async def get_async_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


class CRUDBase():
    def __init__(self, model: Type):
        self.model = model
        
    async def create(self, db: AsyncSession, obj_data: dict):
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def get_all(self, db: AsyncSession) -> List:
        result = await db.execute(select(self.model))
        return result.scalars().all()
    
    async def get_by_id(self, db: AsyncSession, condition):
        result = await db.execute(select(self.model).filter(condition))
        return result.scalars().first()
    
    async def get_by_email(self, db: AsyncSession, condition):
        result = await db.execute(select(self.model).filter(condition))
        return result.scalars().first()
    
    async def update(self, db: AsyncSession, obj_id, update_obj: dict):
        result = await db.execute(select(self.model).filter(self.model.id == obj_id))
        db_obj = result.scalars().first()
        
        if not db_obj:
            return None
        
        for key, value in update_obj.items():
            setattr(db_obj, key, value)
            
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, condition):
        result = await db.execute(select(self.model).filter(condition))
        db_obj = result.scalars().first()
        
        if not db_obj:
            return None
        
        await db.delete(db_obj)
        await db.commit()
        
        return True
    
    
class Users(Base):
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name = Column(VARCHAR(36), nullable=False)
    middle_name = Column(VARCHAR(36), nullable=True)
    last_name = Column(VARCHAR(36), nullable = False)
    email_id = Column(String(256), nullable=False, unique=True)
    mobile_number = Column(String(15), nullable=True)
    password = Column(LONGTEXT, nullable=True)
    otp = Column(String(36), nullable=True)
    mobile_verified = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    access_token = Column(LONGTEXT, nullable=True)
    refresh_token = Column(LONGTEXT, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow())
    
user_model = CRUDBase(Users)