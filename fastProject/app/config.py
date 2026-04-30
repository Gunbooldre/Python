from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ACCESS_KEY: str
    SECRET_KEY_S3: str
    ENDPOINT_URL: str
    BUCKET_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
