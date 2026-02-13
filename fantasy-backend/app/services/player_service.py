from sqlalchemy.orm import Session
from app.models import User, Player
from typing import Optional
from app.repository import player_repo
from app.exceptions import player_exception

def get_all_players(db:Session,limit:int,skip:Optional[int],search: Optional[str]):
    return player_repo.get_player_list(db,limit,skip,search)

def get_player_by_id(db:Session, id: int):
    player = player_repo.get_player_by_id(db,id)
    if player==None:
        raise player_exception.PlayerNotFoundError(f"there is no player of id={id} in the league")
    return player