import os
import ssl
from celery import Celery
from django.conf import settings

# set the default Django settings module for the celery program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'orieng.settings')

app = Celery('orieng', broker=os.getenv('REDIS_TLS_URL'), backend=os.getenv('REDIS_TLS_URL'),
             redis_backend_use_ssl={'ssl_cert_reqs': ssl.CERT_NONE})

app.config_from_object('django.conf:settings', namespace='CELERY')
# app.conf.update(BROKER_URL=os.getenv('REDIS_TLS_URL'), CELERY_RESULT_BACKEND=os.getenv('REDIS_TLS_URL'))
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
