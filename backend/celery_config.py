from celery import Celery
from celery.schedules import crontab

celery = Celery(
    "placement_portal",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.beat_schedule = {

    "daily-placement-reminder": {
        "task": "tasks.daily_reminder_task",
        "schedule": crontab(
            hour=8,
            minute=0
        )
    },

    "monthly-placement-report": {
        "task": "tasks.monthly_report_task",
        "schedule": crontab(
            day_of_month=1,
            hour=9,
            minute=0
        )
    }
}

celery.conf.timezone = "Asia/Kolkata"

# celery -A tasks worker --pool=solo --loglevel=info
# celery -A tasks beat --loglevel=info