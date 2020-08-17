import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'A.settings')

celery_saloon_app = Celery('A')

celery_saloon_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_saloon_app.autodiscover_tasks()