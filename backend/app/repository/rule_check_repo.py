from sqlalchemy.orm import Session
from app.models import Player,TeamPlayer,Team,Slots
from sqlalchemy import func

def get_formation(db:Session, team_id: int):
    return db.query(Team.formation).filter(Team.owner_id == team_id).scalar()

def get_player_count_per_position(db:Session, team_id:int):
    return (db.query(Player.position,func.count(TeamPlayer.player_id))
            .join(Player, Player.id == TeamPlayer.player_id)
            .filter(TeamPlayer.team_id == team_id)
            .group_by(Player.position)
            .all())

def check_slot_taken(db:Session, check_player: TeamPlayer):
    return db.query(TeamPlayer).filter(TeamPlayer.team_id == check_player.team_id, TeamPlayer.slot == check_player.slot).first()

def check_correct_slot_position(db:Session, check_player: TeamPlayer):
    return (db.query(Slots.slot_position)
            .filter(Slots.slot_no == check_player.slot, Slots.team_id == check_player.team_id)
            .one())

def get_player_position(db:Session, check_player:TeamPlayer):
    return (db.query(Player.position)
            .filter(Player.id == check_player.player_id)
            .one())