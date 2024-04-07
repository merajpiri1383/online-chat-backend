from celery import Celery
import os

# set default django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE","core.settings")
# app
app = Celery("app")
# set default configs for app
app.config_from_object("django.conf:settings",namespace="CELERY")
app.conf.broker_connection_retry_on_startup = True
# finding all tasks in installed_apps
app.autodiscover_tasks()