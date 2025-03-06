import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "valify_task.settings")

app = Celery("valify_task")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
