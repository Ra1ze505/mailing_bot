from celery import Celery


def init_celery(broker_url: str) -> Celery:
    return Celery("tasks", broker=broker_url)
