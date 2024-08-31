from celery import Celery
from config import Config

app = Celery('tasks', broker=Config.CELERY_BROKER_URL)
app.conf.update(result_backend=Config.CELERY_RESULT_BACKEND)

# Import tasks to ensure they are registered with Celery
from tasks import image_tasks
