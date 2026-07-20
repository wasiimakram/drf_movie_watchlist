# Import the Celery app whenever Django starts, so @shared_task decorators
# throughout the project connect to THIS app automatically.
from .celery import app as celery_app

__all__ = ('celery_app',)
