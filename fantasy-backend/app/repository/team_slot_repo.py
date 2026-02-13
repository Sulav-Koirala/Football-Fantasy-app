from sqlalchemy.orm import Session
from sqlalchemy import insert
from app.models import Slots

def assign_slots(db:Session, slots: dict):
    db.execute(insert(Slots).values(slots))
    db.commit()

def delete_slots(db:Session, user_id: int):
        return db.query(Slots).filter(Slots.team_id == user_id).delete(synchronize_session=False)

def commit(db:Session):
    db.commit()

def rollback(db:Session):
     db.rollback()

def get_slot_details(db:Session, user_id: int, pos: str):
    return db.query(Slots).filter(Slots.team_id == user_id , Slots.slot_position == pos).order_by(Slots.slot_no).all()