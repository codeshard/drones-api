from sqlmodel import SQLModel, create_engine

from app.settings import get_settings

settings = get_settings()

engine = create_engine(
    url=settings.database_dsn,
    echo=settings.debug,
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
