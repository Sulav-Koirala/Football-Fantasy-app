from sqlalchemy.orm import Session
from app.repository import user_repo
from app.schemas import User_schemas
from app.models import User
from app.utils import utilities
from app.exceptions import user_exception

def get_user(db:Session , id:int):
    user = user_repo.get_user_by_id(db,id)
    if user==None:
        raise user_exception.UserNotFoundError(f"the user with id={id} does not exist.")
    return user

def create_user(db:Session, user: User_schemas.UserInput):
    new_user = User(**user.model_dump())
    existing_user = user_repo.get_user_by_email(db, new_user)
    if existing_user:
        raise user_exception.PreExistingUserError("this user already exists.")
    new_user.password = utilities.hash_pwd(new_user.password)
    return user_repo.create_user(db,new_user)

def delete_user(db:Session, id: int, check_user: User):
    user = user_repo.get_user_by_id(db,id)
    if user==None:
        raise user_exception.UserNotFoundError(f"the user with id={id} does not exist.")
    if user.id != check_user.id:
        raise user_exception.UnauthorizedActionError("you can't delete someone else's account")
    return user_repo.delete_user(db,user)

def update_user_details(db:Session, id: int, updated_user: User_schemas.UserInput, check_user: User):
    user = user_repo.get_user_by_id(db,id)
    if user == None:
        raise user_exception.UserNotFoundError(f"the user with id={id} does not exist.")
    if user.id != check_user.id:
        raise user_exception.UnauthorizedActionError("you can't update someone else's account details")
    for key, value in updated_user.model_dump().items():
        setattr(user, key, value)
    user.password = utilities.hash_pwd(user.password)
    return user_repo.update_user(db,user)