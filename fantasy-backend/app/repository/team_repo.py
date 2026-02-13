from sqlalchemy.orm import Session
from app.models import Team,User
from sqlalchemy.exc import SQLAlchemyError

def create_slot(db:Session, new_team: Team):
    db.add(new_team)
    db.flush()

def get_team_by_owner_id(db: Session,new_team: Team):
    return db.query(Team).filter(Team.owner_id==new_team.owner_id).first()

def create_team(db:Session, new_team: Team):
    db.commit()
    db.refresh(new_team)
    return new_team

def get_team_by_id(db:Session, id: int):
    return db.query(Team).filter(Team.owner_id==id).first()

def delete_team(db:Session, team: Team):
    db.delete(team)
    db.commit()
    return {"message" : "Successfully deleted team"}