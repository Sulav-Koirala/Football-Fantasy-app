from sqlalchemy.orm import Session
from app.models import User,TeamPlayer
from app.schemas import Team_schemas
from . import rule_check_service
from app.exceptions import teamplayer_exception,team_exception
from app.repository import teamplayer_repo,team_repo,player_repo

def sign_player(db:Session, id:int, player: Team_schemas.TeamPlayerInput, check_user:User):
    rule_check_service.check_max_player(db,check_user.id)
    add_player_slot = TeamPlayer(**player.model_dump())
    add_player_slot.team_id = check_user.id
    add_player_slot.player_id = id
    rule_check_service.check_slot_availability(db,add_player_slot)
    existing_add_player = db.query(TeamPlayer).filter(TeamPlayer.team_id == add_player_slot.team_id, TeamPlayer.player_id == add_player_slot.player_id).first()
    if existing_add_player:
        raise teamplayer_exception.PlayerAlreadyInTeamException("this player is already in the team.")
    
    team_name, player_obj, slot, slot_status, slot_role = teamplayer_repo.sign_player_to_team(db,add_player_slot)
    return {
        "team_name": team_name,
        "player_details": player_obj,
        "slot" : slot,
        "slot_status" : slot_status,
        "slot_role" : slot_role
    }

def get_full_team(db:Session,id : int):
    if not team_repo.get_team_by_id(db,id):
        raise team_exception.TeamNotFoundError(f"Team with id {id} does not exist")
    return teamplayer_repo.get_full_team(db,id)

def transfer_player(db:Session, id: int, updated_teamplayer: Team_schemas.TeamPlayerUpdate_Input, check_user: User):
    if not team_repo.get_team_by_id(db,check_user.id) :
        raise team_exception.TeamNotFoundError(f"Team with id {check_user.id} does not exist")
    player_in_team = teamplayer_repo.get_player_in_team(db,id,check_user)
    if not player_in_team:
        raise teamplayer_exception.PlayerNotInTeamError(f"you don't have player of id={id} in your team currently")
    if teamplayer_repo.get_player_in_team(db,updated_teamplayer.player_id,check_user):
        raise teamplayer_exception.TransferError("you cannot transfer the 2 players as both of them are in your team")
    replacing_player = player_repo.get_player_by_id(db, updated_teamplayer.player_id)
    replaced_player = player_repo.get_player_by_id(db,player_in_team.player_id)
    if replaced_player.position != replacing_player.position:
        raise teamplayer_exception.PlayerPositionMismatchError(f"you cannot transfer out a {replaced_player.position} with a {replacing_player.position}")
    for key,value in updated_teamplayer.model_dump().items():
        setattr(player_in_team, key, value)
    return teamplayer_repo.transfer_player(db,player_in_team,check_user,replacing_player)

def substitute_player(db:Session,id : int, sub_player: Team_schemas.TeamPlayerUpdate_Input, check_user: User):
    if not team_repo.get_team_by_id(db,check_user.id) :
        raise team_exception.TeamNotFoundError(f"Team with id {check_user.id} does not exist")
    player_1_in_team = teamplayer_repo.get_player_in_team(db,id,check_user)
    player_2_in_team = teamplayer_repo.get_player_in_team(db,sub_player.player_id,check_user)
    if not (player_1_in_team and player_2_in_team):
        raise teamplayer_exception.PlayerNotInTeamError(f"you don't have one or both player in your team currently")
    player1_status_check = teamplayer_repo.slot_status_check(db,player_1_in_team)
    player2_status_check = teamplayer_repo.slot_status_check(db,player_2_in_team)
    if player1_status_check == player2_status_check:
        raise teamplayer_exception.TransferError(f"you cannot substitute players if they are both {player1_status_check} players")
    sub_player_1 = player_repo.get_player_by_id(db,player_1_in_team.player_id)
    sub_player_2 = player_repo.get_player_by_id(db,player_2_in_team.player_id)
    if sub_player_1.position != sub_player_2.position:
        raise teamplayer_exception.PlayerPositionMismatchError(f"you cannot sub out a {sub_player_1.position} with a {sub_player_2.position}")
    temp_slot = player_1_in_team.slot
    setattr(player_1_in_team, "slot", player_2_in_team.slot)
    setattr(player_2_in_team, "slot", temp_slot)
    return teamplayer_repo.substitute_player(db)

def change_role_slot(db:Session, role_slot: Team_schemas.ChangeRoleInput, check_user: User):
    if not team_repo.get_team_by_id(db,check_user.id) :
        raise team_exception.TeamNotFoundError(f"Team with id {check_user.id} does not exist")
    To_be_VC = teamplayer_repo.get_roled_slot_details(db,check_user,role_slot.vice_captain_slot)
    To_be_Captain = teamplayer_repo.get_roled_slot_details(db,check_user,role_slot.captain_slot)
    if To_be_Captain.slot_role == "Captain" and To_be_VC.slot_role == "Vice Captain" :
        raise teamplayer_exception.RolesAlreadyAssignedError("the given slots are already given the respective roles")
    if To_be_Captain.slot_status == "Bench" or To_be_VC.slot_status == "Bench":
        raise teamplayer_exception.SlotMismatchError("you cant provide these roles to a bench player")
    if To_be_Captain.slot_no == To_be_VC.slot_no:
        raise teamplayer_exception.DoubleRoleError("you cant provide both roles to same player")
    prev_Captain = teamplayer_repo.get_prev_captain_slot(db,check_user)
    prev_VC = teamplayer_repo.get_prev_vc_slot(db,check_user)
    prev_Captain.slot_role = "Member"
    prev_VC.slot_role = "Member"
    To_be_Captain.slot_role = "Captain"
    To_be_VC.slot_role = "Vice Captain"
    return teamplayer_repo.change_role_slots(db)