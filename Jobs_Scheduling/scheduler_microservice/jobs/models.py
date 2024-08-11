from croniter import croniter
from django.db import models
from django.utils import timezone

class Job(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    cron_expression = models.CharField(max_length=100)
    next_run = models.DateTimeField()
    last_run = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'jobs'

    def __str__(self):
        return self.name

    def mark_as_run(self):
        self.last_run = timezone.now()
        self.save()

    def execute(self):
        print(f"Executing job: {self.name}")
        self.last_run = timezone.now()
        cron = croniter(self.cron_expression, self.last_run)
        self.next_run = cron.get_next(timezone.datetime)
        self.save()