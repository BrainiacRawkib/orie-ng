import os
from celery import Celery


# set the default Django settings module for the celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orieng.settings')

app = Celery('orieng')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(BROKER_URL=os.getenv('REDIS_TLS_URL'), CELERY_RESULT_BACKEND=os.getenv('REDIS_TLS_URL'))
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
