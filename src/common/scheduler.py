import asyncio

from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


def init_scheduler() -> AsyncIOScheduler:

    jobstores = {"default": SQLAlchemyJobStore(url="sqlite:///jobs.sqlite")}
    scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="UTC")
    return scheduler
