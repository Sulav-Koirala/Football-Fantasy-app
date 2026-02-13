from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import settings 

engine = create_engine(f"postgresql://{settings.db_username}:{settings.db_pwd}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}")
session_local = sessionmaker(bind = engine, autoflush= False, autocommit = False)
Base = declarative_base()

def db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()