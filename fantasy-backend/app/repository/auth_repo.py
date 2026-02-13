from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.models import User

def get_user_by_email(db:Session , login: OAuth2PasswordRequestForm):
    return db.query(User).filter(User.email == login.username).first()