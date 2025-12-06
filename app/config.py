from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    TARGET_SCHEMA: str
    SOURCE_TABLE1: str
    SOURCE_TABLE2: str
    RESULT_TABLE: str
    TIMEZONE: str

    class Config:
        env_file = ".env"

settings = Settings()

