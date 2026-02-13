from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone
from . import database
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from .config import settings
from app.models import User
from app.schemas import Token_schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE = settings.access_token_expire
SECRET_KEY = settings.secret_key

def create_access_token(data: dict):
    initial_data = data.copy()
    access_expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    initial_data.update({"exp" : access_expire})
    encoded_jwt = jwt.encode (initial_data,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str,exception):
    try :
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id = payload.get("user_id")
        token_data = Token_schemas.TokenData(id = id)
        if id == None:
            raise exception
    except JWTError:
        raise exception
    return token_data

def check_current_user(token: str= Depends(oauth2_scheme), db: Session= Depends(database.db)):
    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Couldn't validate credentials", headers = {"WWW-Authenticate":"Bearer"})
    verify = verify_access_token(token,exception)
    user = db.query(User).filter(User.id==verify.id).first()
    return user