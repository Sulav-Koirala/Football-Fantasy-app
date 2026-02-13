from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_hostname: str
    db_port: str
    db_pwd: str
    db_name: str
    db_username: str
    secret_key: str
    algorithm: str
    access_token_expire: int

    class Config:
        env_file=".env"

settings=Settings()