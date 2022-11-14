import os
from pathlib import Path

from dotenv import load_dotenv


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION")
    ALLOWED_CORS_ORIGINS: str = os.getenv("ALLOWED_CORS_ORIGINS")
    DOCS_URL: str = os.getenv("DOCS_URL")
    REDOC_URL: str = os.getenv("REDOC_URL")

    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    SUPERUSER_USERNAME: str = os.getenv("SUPERUSER_USERNAME")
    SUPERUSER_PASSWORD: str = os.getenv("SUPERUSER_PASSWORD")

    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_TO: str = os.getenv("MAIL_TO")
    MAIL_PORT: str = os.getenv("MAIL_PORT")
    MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME")

    ALGORITHM: str = os.getenv("ALGORITHM")
    JWT_PUBLIC_KEY: str = os.getenv("JWT_PUBLIC_KEY")
    JWT_PRIVATE_KEY: str = os.getenv("JWT_PRIVATE_KEY")

    TKN_EXP_MINS: int = int(os.getenv("TKN_EXP_MINS"))
    ACCES_TKN_EXP_MINS: int = int(os.getenv("ACCES_TKN_EXP_MINS"))
    REFRESH_TKN_EXP_DAYS: int = int(os.getenv("REFRESH_TKN_EXP_DAYS"))


settings = Settings()
