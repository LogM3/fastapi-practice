from time import sleep

from app.tasks.celery import celery_app


@celery_app.task
def count_n(n: int) -> int:
    sleep(5)
    return sum(range(1, n + 1))


@celery_app.task
def send_email(mail_to: str, message: str) -> str:
    sleep(10)
    return f'Message "{message}" sent to {mail_to}'
