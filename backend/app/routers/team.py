from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.core import oauth2
from app.core.database import db
from typing import List
from app.models import Team,User
from app.schemas import Team_schemas
from app.services import team_service
from app.exceptions import team_exception

router = APIRouter(
    prefix="/team",
    tags=["Team"]
)

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=Team_schemas.TeamOutput)
def create_team(team: Team_schemas.TeamInput,db: Session=Depends(db),check_user: User=Depends(oauth2.check_current_user)):
    try:
        return team_service.create_team(db,team,check_user)
    except team_exception.MultipleTeamsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))

@router.get("/",response_model=List[Team_schemas.TeamOutput])
def view_all_teams(db: Session=Depends(db),check_user: User=Depends(oauth2.check_current_user)):
    return team_service.get_all_teams(db)

@router.get("/{id}",response_model=Team_schemas.TeamOutput)
def view_team_by_id(id: int, db: Session=Depends(db),check_user: User=Depends(oauth2.check_current_user)):
    try:
        return team_service.get_team_by_id(db,id)
    except team_exception.TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_team(id: int, db: Session=Depends(db), check_user: User = Depends(oauth2.check_current_user)):
    try:
        return team_service.delete_team(db,id,check_user)
    except team_exception.TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except team_exception.UnauthorizedActionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

@router.put("/{id}",response_model=Team_schemas.TeamOutput)
def update_team_details(id: int, updated_team: Team_schemas.TeamInput, db: Session=Depends(db), check_user: User = Depends(oauth2.check_current_user)):
    try:
        return team_service.update_team_details(db, id, check_user, updated_team)
    except team_exception.TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except team_exception.UnauthorizedActionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))