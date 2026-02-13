from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.core import oauth2
from app.core.database import db
from app.models import User
from app.schemas import User_schemas
from app.services import user_service
from app.exceptions import user_exception

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.get("/{id}",response_model=User_schemas.UserOutput)
def view_user_details(id: int, db: Session= Depends(db), check_user: User=Depends(oauth2.check_current_user)):
    try:
        return user_service.get_user(db,id)
    except user_exception.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    
@router.post("/",response_model=User_schemas.UserOutput,status_code=status.HTTP_201_CREATED)
def create_user(user:User_schemas.UserInput,db: Session=Depends(db)):
    try:
        return user_service.create_user(db,user)
    except user_exception.PreExistingUserError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))
    
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session=Depends(db), check_user: User=Depends(oauth2.check_current_user)):
    try:
        return user_service.delete_user(db,id,check_user)
    except user_exception.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except user_exception.UnauthorizedActionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))
    
@router.put("/{id}",response_model= User_schemas.UserOutput)
def update_user_details(id: int, updated_user: User_schemas.UserInput, db: Session=Depends(db), check_user: User=Depends(oauth2.check_current_user)):
    try:
        return user_service.update_user_details(db,id,updated_user,check_user)
    except user_exception.UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except user_exception.UnauthorizedActionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))