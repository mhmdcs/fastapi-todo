from jose import ExpiredSignatureError, JWSError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# run `openssl rand -hex 32` to gen a long random key
SECRET_KEY = settings.secret_key
ALGORITHM = "HS256" # HMAC SHA256
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(payload: dict):
    plain_payload = payload.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    plain_payload.update({"exp": expire})
    encoded_jwt = jwt.encode(claims=plain_payload, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWSError:
        raise credentials_exception
    except ExpiredSignatureError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Could not validate credentials",
        headers={"WWW-Authenticate:": "Bearer"})
    
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    
    return user