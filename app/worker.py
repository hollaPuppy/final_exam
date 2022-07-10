from celery import Celery

CELERY_BROKER_URL = "redis://redis:5433/0"
CELERY_RESULT_BACKEND = "redis://redis:5433/0"

worker_cel = Celery("celery", backend=CELERY_BROKER_URL, broker=CELERY_RESULT_BACKEND)
