# app/auth.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Use a pure-Python friendly algorithm (avoids bcrypt native issues)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# Example functions used by your project:
def get_password_hash(password: str) -> str:
    # If you must accept very long passwords and later compare with bcrypt, you could truncate.
    # With pbkdf2_sha256 truncation isn't necessary for 72-byte limit.
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# If you also have JWT helpers, keep them (example below is optional)
SECRET_KEY = "change_this_to_a_strong_secret_in_prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data: dict, expires_delta: int | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=(expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
