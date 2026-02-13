from pydantic import BaseModel,Field
from datetime import datetime
from .User_schemas import UserOutput
from .Player_schemas import PlayerOutput
from app.models.Team_models import FormationEnum

class TeamInput(BaseModel):
    team_name: str
    formation: FormationEnum

    model_config={"from_attributes":True}

class TeamOutput(TeamInput):
    owner: UserOutput
    created_at: datetime

    class Config:
        from_attributes = True

class TeamPlayerInput(BaseModel):
    slot : int = Field(ge=1, le=15)

class TeamPlayerOutput(BaseModel):
    team_name : str
    player_details : PlayerOutput
    slot : int
    slot_status : str
    slot_role : str

    class Config:
        from_attributes = True

class TeamPlayerUpdate_Input(BaseModel):
    player_id : int

class TeamPlayerUpdate_Output(BaseModel):
    id : int
    first_name : str
    last_name : str
    club : str
    position: str
    status : str
    role : str

    class Config:
        from_attributes = True

class ChangeRoleInput(BaseModel):
    captain_slot: int
    vice_captain_slot: int