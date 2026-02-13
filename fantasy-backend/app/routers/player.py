from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.core import oauth2
from app.core.database import db
from typing import List, Optional
from app.models import User
from app.schemas import Player_schemas
from app.services import player_service
from app.exceptions import player_exception

router = APIRouter(
    prefix= "/player",
    tags= ["Player"]
)

@router.get("/",response_model=List[Player_schemas.PlayerOutput])
def view_player_list(db: Session=Depends(db), check_user: User=Depends(oauth2.check_current_user), limit: int = 10, skip: Optional[int] = 0, search: Optional[str]=""):
    return player_service.get_all_players(db,limit,skip,search)

@router.get("/{id}",response_model=Player_schemas.PlayerOutput)
def view_player_by_id(id: int, db: Session=Depends(db), check_user: User=Depends(oauth2.check_current_user)):
    try:
        return player_service.get_player_by_id(db,id)
    except player_exception.PlayerNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))