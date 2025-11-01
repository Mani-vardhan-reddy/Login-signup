from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY : str
    ALGORITHM: str
    MAX_OTP_COUNT: int
    OTP_VALID_FOR_SECONDS: int
    
    class Config:
        env_file = ".env"
        
settings = Settings()