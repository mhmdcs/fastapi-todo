from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_connection_string: str
    secret_key: str

    class Config:
        env_file = ".env"

settings = Settings()
