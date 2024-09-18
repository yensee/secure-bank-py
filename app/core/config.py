from pydantic import BaseSettings

class Settings(BaseSettings):
    # SQLALCHEMY_DATABASE_URL: str = "postgresql://user:password@localhost/account_db"
    SQLALCHEMY_DATABASE_URL: str = "mysql+pmysql://user:password@localhost/account_db"
    class Config:
        env_file = ".env"

settings = Settings()
