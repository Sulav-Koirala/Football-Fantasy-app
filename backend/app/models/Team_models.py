from app.core.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text, ForeignKey,Enum, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
import enum

class FormationEnum(str, enum.Enum):
    F_352 = "3-5-2"
    F_343 = "3-4-3"
    F_451 = "4-5-1"
    F_442 = "4-4-2"
    F_433 = "4-3-3"
    F_541 = "5-4-1"
    F_532 = "5-3-2"
    F_523 = "5-2-3"

class Team(Base):
    __tablename__ = "Teams"
    owner_id = Column(Integer,ForeignKey("Users.id", ondelete="CASCADE"),primary_key=True)
    owner = relationship("User")
    team_name = Column(String, nullable = False)
    formation = Column(Enum(FormationEnum, name="formation_enum"), nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))

class TeamPlayer(Base):
    __tablename__ = "Team_Players"
    team_id = Column(Integer,ForeignKey("Teams.owner_id", ondelete="CASCADE"),primary_key=True)
    owner = relationship("Team")
    player_id = Column(Integer,ForeignKey("Players.id", ondelete="CASCADE"),primary_key=True)
    relation = relationship("Player")
    slot = Column(Integer, CheckConstraint("slot>=1 AND slot<=15", name= "slot_range_check"), nullable=False)

    __table_args__ = (
        UniqueConstraint("team_id", "slot", name="unique_slot_per_team"),
    )

class Slots(Base):
    __tablename__ = "player_slots"
    team_id = Column(Integer,ForeignKey("Teams.owner_id", ondelete="CASCADE"),primary_key=True)
    owner = relationship("Team")
    slot_no = Column(Integer, CheckConstraint("slot_no >=1 AND slot_no <=15", name= "slot_range_check"), primary_key=True)
    slot_position = Column(String(2),CheckConstraint("slot_position IN ('GK' , 'DF' , 'MF' , 'FW')", name = "slot_postition_check"), nullable = False)
    slot_status = Column(String, CheckConstraint("slot_status IN ('Starting' , 'Bench')", name="slot_status_check"),nullable = False)
    slot_role = Column(String, CheckConstraint("slot_role IN ('Captain' , 'Vice Captain' , 'Member')", name="slot_role_check"),nullable = False)