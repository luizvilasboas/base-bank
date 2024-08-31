from celery import Celery
import os

import tasks.transaction_tasks

celery_app = Celery(__name__)
celery_app.conf.broker_url = "redis://redis:6379/0"
celery_app.conf.result_backend = "redis://redis:6379/0"
