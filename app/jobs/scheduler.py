from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit

scheduler = BackgroundScheduler()

def schedule_job(func, cron_expression, *args, **kwargs):
    """Schedule a job using cron expression"""
    job = scheduler.add_job(
        func=func,
        trigger=CronTrigger.from_crontab(cron_expression),
        args=args,
        kwargs=kwargs
    )
    return job.id

def start_scheduler():
    scheduler.start()
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())