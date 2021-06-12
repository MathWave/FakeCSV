import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
from FakeCSV import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FakeCSV.settings')

app = Celery('FakeCSV')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(BROKER_URL=os.getenv('REDIS_URL', settings.CELERY_BROKER_URL))

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
