from __future__ import absolute_import
import os

from django.conf import settings
from celery import Celery

from backend.settings import (RABBITMQ_USER, RABBITMQ_PASS)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
app = Celery('CeleryApp')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.update(
    BROKER_URL='amqp://' +
    RABBITMQ_USER +
    ':' +
    RABBITMQ_PASS +
    '@localhost:5672//',
)
