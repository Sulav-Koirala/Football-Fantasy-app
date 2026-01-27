from sqlalchemy.orm import Session
from app.models import Player,User
from typing import Optional

def get_player_list(db:Session,limit:int,skip:Optional[int],search: Optional[str]):
    return db.query(Player).filter(Player.position.contains(search)).limit(limit).offset(skip).all()

def get_player_by_id(db:Session,id:int):
    return db.query(Player).filter(Player.id==id).first()