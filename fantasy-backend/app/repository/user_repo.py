from sqlalchemy.orm import Session
from app.models import User

def create_user(db:Session, new_user: User):
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def delete_user(db:Session, user: User):
    db.delete(user)
    db.commit()
    return {"message" : "Successfully deleted user"}

def update_user(db:Session, user: User):
    db.commit()
    db.refresh(user)
    return user

def get_user_by_id(db:Session , id: int):
    return db.query(User).filter(User.id==id).first()

def get_user_by_email(db:Session, new_user: User):
    return db.query(User).filter(User.email==new_user.email).first()
