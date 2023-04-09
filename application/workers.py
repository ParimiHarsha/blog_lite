from celery import Celery
from celery.schedules import crontab
from flask import current_app as app

celery = Celery("backend jobs")
celery.conf.imports = ["application.tasks"]

celery.conf.beat_schedule = {
    "send-monthly-engagement-report": {
        "task": "application.tasks.send_email",
        "schedule": crontab(hour=12, minute=30, day_of_month=1),
    },
    "send-everyday-at-6pm": {
        "task": "application.tasks.daily_reminder",
        "schedule": crontab(hour=12, minute=30),
    },
}
celery.conf.timezone = "UTC"


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
