from pydantic import BaseModel

class PlayerOutput(BaseModel):
    id : int
    first_name : str
    last_name : str
    nationality : str
    club : str
    position : str

    class Config:
        from_attributes = True