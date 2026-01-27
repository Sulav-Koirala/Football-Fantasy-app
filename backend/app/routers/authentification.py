from fastapi import Depends,HTTPException,status,APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import db
from app.schemas import Token_schemas
from app.services import auth_service
from app.exceptions.auth_exception import InvalidCredentialsError

router = APIRouter(
    prefix = "/login",
    tags = ["Authentification"]
)

@router.post("/", response_model= Token_schemas.Token)
def login_user(db: Session=Depends(db), login: OAuth2PasswordRequestForm=Depends()):
    try:
        return auth_service.login_user(db,login)
    except InvalidCredentialsError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))