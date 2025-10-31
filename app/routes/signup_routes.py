from fastapi import APIRouter, HTTPException, status, Depends
from app.models.signup_models import get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.signup_schemas import SignUp, CreatePassword, MobileAdd, MobileOTPVerify
from app.services.signup_services import signup_service

router = APIRouter()

@router.post("/signup", tags=['SignUp'])
async def user_signup(payload: SignUp, session: AsyncSession = Depends(get_async_db)):
    try:
        response = await signup_service.signup(payload, session)
        return response
    except HTTPException as http_exe:
        raise http_exe
    except Exception as e:
        raise e

@router.post("/create-password", tags=['SignUp'])
async def create_password(payload: CreatePassword, session: AsyncSession = Depends(get_async_db)):
    try:
        response = await signup_service.create_password(payload, session)
        return response
    except HTTPException as http_exe:
        raise http_exe
    except Exception as e:
        raise e
    
@router.post("/add-mobile-number", tags=['SignUp'])
async def add_mobile_number(payload: MobileAdd, session: AsyncSession = Depends(get_async_db)):
    try:
        response = await signup_service.add_mobile_number(payload, session)
        return response
    except HTTPException as http_exe:
        raise http_exe
    except Exception as e:
        raise e
    
@router.post("/verify-mobile", tags=['SignUp'])
async def verify_mobile(payload: MobileOTPVerify, session: AsyncSession = Depends(get_async_db)):
    try:
        response = await signup_service.verify_mobile_otp(payload, session)
        return response
    except HTTPException as http_exe:
        raise http_exe
    except Exception as e:
        raise e
    
@router.get("/generate-otp/{user_id}", tags=['Generate OTP'])
async def generate_otp(user_id: str, session: AsyncSession = Depends(get_async_db)):
    try:
        response = await signup_service.generete_otp(session, user_id)
        return response
    except HTTPException as http_exe:
        raise http_exe
    except Exception as e:
        raise e