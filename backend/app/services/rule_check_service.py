from sqlalchemy.orm import Session
from app.models import TeamPlayer
from app.repository import rule_check_repo
from app.exceptions import teamplayer_exception,team_exception

MAX_PLAYERS = 15

def check_max_player(db: Session, team_id: int):
     if not rule_check_repo.get_formation(db,team_id):
          raise team_exception.TeamNotFoundError("Team not created")
    
     counts = rule_check_repo.get_player_count_per_position(db,team_id)

     position_counts = {pos: count for pos, count in counts}
     total_players = sum(position_counts.values())

     if total_players >= MAX_PLAYERS:
          raise teamplayer_exception.MaximumPlayerLimit("Maximum number of players reached")

def check_slot_availability(db:Session,check_player: TeamPlayer):
     if rule_check_repo.check_slot_taken(db,check_player):
         raise teamplayer_exception.SlotAlreadyTakenError("this slot is already taken by another player")
     correct_slot_position = rule_check_repo.check_correct_slot_position(db,check_player)
     player_position = rule_check_repo.get_player_position(db,check_player)
     if  correct_slot_position != player_position :
         raise teamplayer_exception.SlotMismatchError(f"you cannot include a player of position {player_position[0]} in a slot for {correct_slot_position[0]}")
