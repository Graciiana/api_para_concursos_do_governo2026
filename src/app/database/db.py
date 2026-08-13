from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings


engine = create_engine(settings.data_base)
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def get_session_db():
    with SessionLocal() as session:
        yield session
