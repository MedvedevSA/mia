from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: str = '5432'
    DB_NAME: str = 'postgres'
    DB_USER: str = 'postgres'
    DB_PASS: str = 'mysecretpassword'

    SRV_HOST: str = "0.0.0.0"
    SRV_PORT: int = 8000


settings = Settings()

DATABASE_URL = 'postgresql+asyncpg://{}:{}@{}:{}/{}'.format(
    settings.DB_USER,
    settings.DB_PASS,
    settings.DB_HOST,
    settings.DB_PORT,
    settings.DB_NAME
)
