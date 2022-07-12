import os
from celery import Celery

CONFIG_CELERY_BROKER_URL: str = os.getenv('CELERY_BROKER_URL')
if not CONFIG_CELERY_BROKER_URL:
    CONFIG_CELERY_BROKER_URL = "redis://localhost:6379/0"

CONFIG_CELERY_RESULT_BACKEND: str = os.getenv('CELERY_RESULT_BACKEND')
if not CONFIG_CELERY_RESULT_BACKEND:
    CONFIG_CELERY_RESULT_BACKEND = "redis://localhost:6379/0"


worker_cel = Celery("celery", backend=CONFIG_CELERY_RESULT_BACKEND, broker=CONFIG_CELERY_BROKER_URL)
