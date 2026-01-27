from sqlalchemy.orm import Session
from app.models import User,TeamPlayer,Slots,Team,Player
from sqlalchemy import select,and_

def sign_player_to_team(db:Session, add_player_slot: TeamPlayer):
    db.add(add_player_slot)
    db.commit()
    db.refresh(add_player_slot)
    signed = (db.query(Team.team_name, Player, TeamPlayer.slot, Slots.slot_status , Slots.slot_role )
            .join(Team,Team.owner_id == TeamPlayer.team_id)
            .join(Player,Player.id == TeamPlayer.player_id)
            .join(Slots, and_(Slots.team_id == TeamPlayer.team_id , Slots.slot_no == TeamPlayer.slot))
            .filter(TeamPlayer.team_id == add_player_slot.team_id, TeamPlayer.player_id == add_player_slot.player_id)
            .first())
    return signed

def get_full_team(db:Session, id:int):
    view = (select(TeamPlayer.player_id.label("id"),
                Player.first_name.label("first_name"),
                Player.last_name.label("last_name"),
                Player.club.label("club"),
                Player.position.label("position"),
                Slots.slot_status.label("status"),
                Slots.slot_role.label("role"))
            .join(Player, Player.id == TeamPlayer.player_id)
            .join(Slots, and_(Slots.team_id == TeamPlayer.team_id,Slots.slot_no == TeamPlayer.slot))
            .where(TeamPlayer.team_id == id))
    return db.execute(view).mappings().all()

def get_player_in_team(db:Session, id:int, check_user: User):
    return db.query(TeamPlayer).filter(TeamPlayer.team_id == check_user.id , TeamPlayer.player_id == id).first()

def transfer_player(db:Session,player_in_team: TeamPlayer,check_user:User, replacing_player: Player):
    db.commit()
    db.refresh(player_in_team)
    view = (select(TeamPlayer.player_id.label("id"),
                Player.first_name.label("first_name"),
                Player.last_name.label("last_name"),
                Player.club.label("club"),
                Player.position.label("position"),
                Slots.slot_status.label("status"),
                Slots.slot_role.label("role"))
            .join(Player, Player.id == TeamPlayer.player_id)
            .join(Slots, (Slots.team_id == TeamPlayer.team_id) & (Slots.slot_no == TeamPlayer.slot))
            .where(TeamPlayer.team_id == check_user.id , TeamPlayer.player_id == replacing_player.id))
    return db.execute(view).mappings().first()

def slot_status_check(db: Session, player_in_team: TeamPlayer):
    return (db.query(Slots.slot_status).select_from(TeamPlayer)
            .join(Slots,(Slots.team_id == TeamPlayer.team_id) & (Slots.slot_no == TeamPlayer.slot))
            .filter(TeamPlayer.player_id == player_in_team.player_id)
            .scalar())

def substitute_player(db:Session):
    db.commit()
    return {"message" : "Successfully substituted player"}

def get_roled_slot_details(db:Session,check_user: User, role_slot: int):
    return db.query(Slots).filter(Slots.team_id == check_user.id, Slots.slot_no == role_slot).first()

def get_prev_captain_slot(db:Session,check_user:User):
    return db.query(Slots).filter(Slots.team_id == check_user.id, Slots.slot_role == "Captain").one()

def get_prev_vc_slot(db:Session,check_user:User):
    return db.query(Slots).filter(Slots.team_id == check_user.id, Slots.slot_role == "Vice Captain").one()

def change_role_slots(db:Session):
    db.commit()
    return {"message" : "Successfully updated Captain and Vice Captain roles"}