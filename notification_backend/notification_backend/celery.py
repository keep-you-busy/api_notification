import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'notification_backend.settings')
app = Celery('notification_backend')
app.config_from_object('django.conf:settings',
                       namespace='CELERY')
app.autodiscover_tasks()
