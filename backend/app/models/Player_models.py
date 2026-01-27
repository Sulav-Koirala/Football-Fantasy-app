from app.core.database import Base
from sqlalchemy import Column, Integer, String

class Player(Base):
    __tablename__ = "Players"
    id = Column(Integer,primary_key=True)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    nationality = Column(String,nullable=False)
    club = Column(String,nullable=False)
    position = Column(String,nullable=False)