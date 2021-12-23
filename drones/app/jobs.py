from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.settings import get_settings

settings = get_settings()


def _create_schedule() -> AsyncIOScheduler:
    try:
        jobstores = {
            "default": SQLAlchemyJobStore(
                url=settings.database_dsn.replace(
                    "+asyncpg", ""
                ),  # dirty fix, still not available until aps v4
            )
        }
        schedule = AsyncIOScheduler(jobstores=jobstores)
        return schedule
    except Exception as e:
        raise e


global schedule
schedule = _create_schedule()
