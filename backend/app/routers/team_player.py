from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from app.core import oauth2
from app.core.database import db
from app.models import User
from app.schemas import Team_schemas
from app.services import teamplayer_service
from app.exceptions import teamplayer_exception,team_exception

router = APIRouter(
    prefix="/teamplayer",
    tags= ["Team_Player"]
)

@router.post("/sign/{id}",status_code=status.HTTP_201_CREATED,response_model=Team_schemas.TeamPlayerOutput)
def sign_player_to_team(id: int, player: Team_schemas.TeamPlayerInput, db:Session=Depends(db),check_user: User=Depends(oauth2.check_current_user)):
    try:
        return teamplayer_service.sign_player(db,id,player,check_user)
    except team_exception.TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except teamplayer_exception.MaximumPlayerLimit as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))
    except teamplayer_exception.PlayerAlreadyInTeamException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except teamplayer_exception.SlotAlreadyTakenError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except teamplayer_exception.SlotMismatchError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=str(e))

@router.get("/{id}")
def view_a_full_team(id: int, db: Session=Depends(db), check_user: User=Depends(oauth2.check_current_user)):
    try:
        return teamplayer_service.get_full_team(db,id)
    except team_exception.TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))

@router.put("/sign/{id}", response_model=Team_schemas.TeamPlayerUpdate_Output)
def transfer_team_player(id: int, updated_teamplayer: Team_schemas.TeamPlayerUpdate_Input , db: Session=Depends(db), check_user: User=Depends(oauth2.check_current_user)):
    try:
        return teamplayer_service.transfer_player(db,id,updated_teamplayer,check_user)
    except team_exception.TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except teamplayer_exception.PlayerNotInTeamError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except teamplayer_exception.TransferError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except teamplayer_exception.PlayerPositionMismatchError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    

@router.put("/{id}")
def substitute_team_player(id: int, sub_player: Team_schemas.TeamPlayerUpdate_Input, db: Session=Depends(db),check_user: User=Depends(oauth2.check_current_user)):
    try:
        return teamplayer_service.substitute_player(db,id,sub_player,check_user)
    except team_exception.TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except teamplayer_exception.PlayerNotInTeamError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except teamplayer_exception.TransferError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except teamplayer_exception.PlayerPositionMismatchError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    

@router.put("/role/")
def change_captain_vc(role_slot: Team_schemas.ChangeRoleInput, db: Session=Depends(db),check_user: User=Depends(oauth2.check_current_user)):
    try:
        return teamplayer_service.change_role_slot(db,role_slot,check_user)
    except team_exception.TeamNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=str(e))
    except teamplayer_exception.RolesAlreadyAssignedError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))
    except teamplayer_exception.SlotMismatchError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))
    except teamplayer_exception.DoubleRoleError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))