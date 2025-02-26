import os
from typing import Tuple, List, Dict

from celery import Celery
from celery.schedules import crontab

from . import settings 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.core.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = 'Europe/Moscow'

def is_task_with_params_running(args):
    inspector = app.control.inspect()

    tasks_data = {}
    tasks_data.update(inspector.active() or {})
    tasks_data.update(inspector.reserved() or {})
    tasks_data.update(inspector.scheduled() or {})
    
    
    for worker, tasks in tasks_data.items():
        for task in tasks:
            if task['request'].get('args') == args:
                return True
            
    return False
