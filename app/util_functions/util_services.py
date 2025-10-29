from passlib.context import CryptContext
import random
import secrets
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.database.config import settings


password_hasher = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(plain_password):
    return password_hasher.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return password_hasher.verify(plain_password, hashed_password)

def generate_otp():
    return random.randint(100000,999999)

def generate_secret_otp():
    return secrets.randbelow(900000) + 100000

async def create_token(data: dict, expire_time = None):
    try:
        token_data = data.copy()
        expire_time = expire_time if expire_time else timedelta(hours=24)
        token_data.update({"exp": datetime.utcnow() + expire_time})
        token = jwt.encode(token_data, settings.SECRET_KEY, settings.ALGORITHM)
        return token
    except Exception as e:
        raise e
    
async def verify_token(token):
    try:
        decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return decode_data
    except Exception as e:
        raise e