from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY : str
    ALGORITHM: str
    MAX_OTP_COUNT: int
    OTP_VALID_FOR_SECONDS: int
    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_OFFSET_RESET: str
    KAFKA_RETRIES: int
    
    class Config:
        env_file = ".env"
        
settings = Settings()