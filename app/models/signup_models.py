from app.database.database import Base
from sqlalchemy import Column, String, VARCHAR, INTEGER, Boolean, DateTime, String
from sqlalchemy.dialects.mysql import LONGTEXT
from datetime import datetime
from app.models.crud import CRUDBase
import uuid
from app.database.database import SessionLocal

async def get_async_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
    
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
    otp_count = Column(INTEGER, nullable=True, default=0)
    otp_created_at = Column(DateTime, nullable=True)
    resend_otp_time = Column(DateTime, nullable= True)
    mobile_verified = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    access_token = Column(LONGTEXT, nullable=True)
    refresh_token = Column(LONGTEXT, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow())
    
user_model = CRUDBase(Users)