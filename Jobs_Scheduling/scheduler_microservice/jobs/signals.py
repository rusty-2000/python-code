from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Job
from django.core.cache import cache
from django.utils import timezone
from croniter import croniter


def connect_signals():
    @receiver(post_save, sender=Job)
    def invalidate_job_cache(sender, instance, **kwargs):
        cache.delete('job_list')