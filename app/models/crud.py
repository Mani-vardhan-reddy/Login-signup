from sqlalchemy.ext.asyncio import AsyncSession
from typing import Type, List, Optional
from sqlalchemy.future import select


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