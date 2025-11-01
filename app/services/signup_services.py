from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from app.models.signup_models import user_model, Users
from app.database.constants import ResponseMessage
from app.util_functions.util_services import hash_password, generate_secret_otp
from app.database.config import settings

class SignUpService():
    async def signup(self, payload, session):
        try:
            user_details = await user_model.get_by_email(session, Users.email_id == payload.email_id)
            if user_details:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessage.USER_ALREADY_EXIST)
            
            response = await user_model.create(session, payload.model_dump())
            
            return {"user_id": response.id}
        
        except HTTPException as http_exe:
            raise http_exe
        except Exception as e:
            raise e
        
    async def create_password(self, payload, session):
        try:
            user_details = await user_model.get_by_id(session, Users.id == str(payload.user_id))
            if not user_details:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessage.USER_NOT_FOUND)
            
            if user_details.password:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessage.PASSWORD_SET_ALREADY)
            
            if payload.new_password != payload.confirm_password:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessage.PASSWORD_NOT_MATCH)
            
            hashed = hash_password(payload.new_password)
            
            await user_model.update(session, str(payload.user_id), {"password": hashed})
            
            return {"user_id": payload.user_id}
        
        except HTTPException as http_exe:
            raise http_exe
        except Exception as e:
            raise e
        
    async def add_mobile_number(self, payload, session):
        try:
            user_details = await user_model.get_by_id(session, Users.id == str(payload.user_id))
            if not user_details:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessage.USER_NOT_FOUND)
            
            if user_details.mobile_number:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessage.MOBILE_NUMBER_ALREADY_SET)
            
            await user_model.update(session, str(payload.user_id), {"mobile_number": payload.mobile_number})
            
            return {"user_id": payload.user_id}
        
        except HTTPException as http_exe:
            raise http_exe
        except Exception as e:
            raise e
        
    async def verify_mobile_otp(self, payload, session):
        try:
            user_details = await user_model.get_by_id(session, Users.id == str(payload.user_id))
            
            if not user_details:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessage.USER_NOT_FOUND)
            
            if user_details.otp != payload.otp:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessage.INVALID_OTP)
            
            if not user_details.otp_created_at:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessage.OTP_NOT_CREATED)
            
            if (datetime.utcnow() - user_details.otp_created_at).total_seconds() > settings.OTP_VALID_FOR_SECONDS:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessage.OTP_EXPIRED)
            
            update_payload = {
                "otp": None,
                "otp_count": 0,
                "resend_otp_time": None,
                "mobile_verified": True
            }
            
            await user_model.update(session, str(payload.user_id), update_payload)
            
            return {"user_id": payload.user_id}
        
        except HTTPException as http_exe:
            raise http_exe
        except Exception as e:
            raise e
        
    async def generete_otp(self, session, user_id):
        try:
            user_details = await user_model.get_by_id(session, Users.id == str(user_id))
            
            if not user_details:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessage.USER_NOT_FOUND)
            
            otp_count = 1
            if user_details.otp_count:
                otp_count += user_details.otp_count
                
            if otp_count > settings.MAX_OTP_COUNT and user_details.resend_otp_time == None:
                await user_model.update(
                    session, 
                    str(user_id), 
                    {
                        "otp":None, 
                        "otp_count": 0, 
                        "otp_created_at": None, 
                        "resend_otp_time":datetime.utcnow() + timedelta(minutes=30)
                    }
                )
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=ResponseMessage.OTP_COUNT_REACHED)
            
            if user_details.resend_otp_time and user_details.resend_otp_time > datetime.utcnow():
                remaining = (user_details.resend_otp_time - datetime.utcnow()).seconds // 60
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Resend time not completed. Try again after {remaining} minutes")
            
            otp = generate_secret_otp()
            
            await user_model.update(
                session, 
                str(user_id), 
                {
                    "otp":otp, "otp_count": otp_count, 
                    "otp_created_at": datetime.utcnow(), 
                    "resend_otp_time":None, 
                }
            )
            
            return otp
        
        except HTTPException as http_exe:
            raise http_exe
        except Exception as e:
            raise e
        
signup_service = SignUpService()