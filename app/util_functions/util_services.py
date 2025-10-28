from passlib.context import CryptContext
import random
import secrets


password_hasher = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(plain_password):
    return password_hasher.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return password_hasher.verify(plain_password, hashed_password)

def generate_otp():
    return random.randint(100000,999999)

def generate_secret_otp():
    return secrets.randbelow(900000) + 100000