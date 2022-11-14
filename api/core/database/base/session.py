from typing import Generator

from core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DB_URL)

# SQLALCHEMY_DB_URL = 'sqlite:///core/database/./sqlite_db.db'
# engine = create_engine(
#     SQLALCHEMY_DB_URL, connect_args={'check_same_thread': False}
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
