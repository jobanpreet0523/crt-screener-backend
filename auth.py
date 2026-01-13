import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

SECRET = "CHANGE_THIS_SECRET"
ALGO = "HS256"

pwd = CryptContext(schemes=["bcrypt"])

def hash_pw(p):
    return pwd.hash(p)

def verify_pw(p, h):
    return pwd.verify(p, h)

def create_token(username):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)

def decode_token(token):
    return jwt.decode(token, SECRET, algorithms=[ALGO])["sub"]
