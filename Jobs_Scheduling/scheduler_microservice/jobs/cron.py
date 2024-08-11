
import logging
from django.db import transaction
from django.utils import timezone
from django_cron import CronJobBase, Schedule
from croniter import croniter
from .models import Job

logger = logging.getLogger(__name__)


class RunScheduledJobs(CronJobBase):
    RUN_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'jobs.run_scheduled_jobs'

    def do(self):
        now = timezone.now()
        jobs = Job.objects.filter(is_active=True, next_run__lte=now)

        for job in jobs:
            try:
                with transaction.atomic():
                    # Execute job (dummy implementation)
                    logger.info(f"Executing job: {job.name}")
                    # Here you would typically call a task queue like Celery
                    # to handle the actual job execution asynchronously

                    # Update last_run and calculate next_run
                    job.last_run = now
                    cron = croniter(job.cron_expression, now)
                    job.next_run = cron.get_next(timezone.datetime)
                    job.save()
            except Exception as e:
                logger.error(f"Error executing job {job.name}: {str(e)}")