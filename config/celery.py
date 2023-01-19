from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
#from config.settings.base import 
#from app.articles.models import Article

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()