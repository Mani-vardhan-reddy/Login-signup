from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY : str
    ALGORITHM: str
    MAX_OTP_COUNT: int
    OTP_VALID_FOR_SECONDS: int
    
    KAFKA_EMAIL_TOPIC: str
    KAFKA_GROUP_ID: str
    KAFKA_AUTO_OFFSET_RESET: str
    KAFKA_BROKER_URL: str
    
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_FROM_EMAIL: str
    SMTP_FROM_NAME: str
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    
    GOOGLE_AUTH_ENDPOINT: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_TOKEN_ENDPOINT: str
    GOOGLE_USER_ENDPOINT: str
    GOOGLE_REDIRECT_URI: str
    
    class Config:
        env_file = ".env"
        
settings = Settings()