from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.core import oauth2
from app.repository import auth_repo
from app.utils import utilities
from app.exceptions.auth_exception import InvalidCredentialsError

def login_user(db:Session, login: OAuth2PasswordRequestForm):
    user = auth_repo.get_user_by_email(db,login)
    if not user or not utilities.verify_pwd(login.password,user.password):
        raise InvalidCredentialsError("Username or Password is incorrect")
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    return {"token" : access_token,
            "token_type" : "Bearer"}