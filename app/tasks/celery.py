from celery import Celery

from app.settings import settings


def make_celery() -> Celery:
    celery: Celery = Celery(
        'worker',
        broker=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0',
        backend=f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/1'
    )

    celery.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True
    )

    return celery


celery_app: Celery = make_celery()

celery_app.autodiscover_tasks(['app.tasks.tasks'])
