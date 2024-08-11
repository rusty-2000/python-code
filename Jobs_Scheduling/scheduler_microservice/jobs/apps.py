from django.apps import AppConfig
from .models import Job
class JobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jobs'
    label = 'jobs'

    def ready(self):
        try:
            import jobs.signals
        except ImportError:
            pass
    # def ready(self):
    #     from .signals import connect_signals
    #     connect_signals()