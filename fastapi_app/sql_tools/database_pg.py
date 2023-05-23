from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from fastapi_app.fastapp import app
from fastapi_app.core.config import settings

engine = create_engine(
    settings.database_url, pool_size=20, max_overflow=0
)

Session = sessionmaker(bind=engine,
                       autocommit=False,
                       autoflush=False,
                       )

Base = declarative_base()


def get_session():
    db = Session()
    try:
        yield db
    finally:
        db.close()
