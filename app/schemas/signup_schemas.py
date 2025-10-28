from pydantic import BaseModel,EmailStr
from typing import Optional
from uuid import UUID

class SignUp(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email_id: EmailStr
    
class CreatePassword(BaseModel):
    user_id: UUID
    new_password: str
    confirm_password: str
    
class MobileAdd(BaseModel):
    user_id: UUID
    mobile_number: str
    
class MobileOTPVerify(BaseModel):
    user_id: UUID
    otp: str