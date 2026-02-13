from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import User,Team
from app.schemas import Team_schemas
from app.repository import team_repo
from app.exceptions import team_exception
from . import team_slot_service

def create_team(db:Session, team: Team_schemas.TeamInput, check_user: User):
    new_team = Team(**team.model_dump())
    new_team.owner_id = check_user.id
    existing_team = team_repo.get_team_by_owner_id(db,new_team)
    if existing_team:
        raise team_exception.MultipleTeamsError("you already have a team, cannot create more than one team per user")
    try:
        team_repo.create_slot(db,new_team)
        team_slot_service.assign_slots(db, new_team.formation, check_user.id)
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    return team_repo.create_team(db,new_team)

def get_all_teams(db:Session):
    return db.query(Team).all()

def get_team_by_id(db:Session, id: int):
    team = team_repo.get_team_by_id(db,id)
    if team==None:
        raise team_exception.TeamNotFoundError(f"no such team of owner_id={id} exists.")
    return team

def delete_team(db:Session, id: int, check_user: User):
    team = team_repo.get_team_by_id(db,id)
    if id==check_user.id and team == None :
        raise team_exception.TeamNotFoundError("you dont have a team yet")
    if id != check_user.id:
        raise team_exception.UnauthorizedActionError("you cannot delete a team of another user")
    return team_repo.delete_team(db,team)

def update_team_details(db:Session, id: int, check_user: User, updated_team: Team_schemas.TeamInput):
    team = team_repo.get_team_by_id(db,id)
    if id == check_user.id and team == None:
        raise team_exception.TeamNotFoundError("you dont have a team yet")
    if id != check_user.id :
        raise team_exception.UnauthorizedActionError("you can't update someone else's account details")
    for key, value in updated_team.model_dump().items():
        setattr(team, key, value)
    team_slot_service.arrange_slots(db, team.formation, check_user.id)
    return team_repo.create_team(db,team)