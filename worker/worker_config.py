from celery import Celery


worker_cel = Celery("celery", backend="redis://localhost:6379/1", broker="redis://localhost:6379/1")
