from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UserInput(BaseModel):
    email : EmailStr
    password : str

    @field_validator("email")
    @classmethod
    def gmail_only(cls, email: EmailStr):
        if not email.lower().endswith("@gmail.com"):
            raise ValueError("Only Gmail addresses are allowed")
        return email.lower()

class UserOutput(BaseModel):
    id : int
    email: EmailStr
    created_at : datetime

    class Config:
        from_attributes = True