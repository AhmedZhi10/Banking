from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv # استيراد دالة لتحميل المتغيرات
from pathlib import Path
import os
# --- NEW: Load environment variables from .env file ---
# We assume the .env file is in the root directory, one level above 'transaction_service'
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)
# ----------------------------------------------------


# --- UPDATED: Read secret key from environment ---
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("DJANGO_SECRET_KEY not found in environment variables")
# ------------------------------------------------
# --- THE FIX IS HERE ---
# The algorithm name was corrected from "HS2HS256" to "HS256".
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user_id(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        raw_user_id = payload.get("user_id")
        if raw_user_id is None:
            raise credentials_exception
        
        user_id = int(raw_user_id)

    except (JWTError, ValueError):
        raise credentials_exception
    
    return user_id

