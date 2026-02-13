from app.core.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, text

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False,unique=True)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))