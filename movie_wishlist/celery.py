"""
Concept #36 — Celery: background tasks that run OUTSIDE the request/response
cycle, in a separate process, so slow work (calling OMDB, sending email)
doesn't make the user wait.

THE MOVING PIECES (3 processes, all must be running):

  1. Django (runserver)     — receives the HTTP request, calls .delay(),
                               returns a response IMMEDIATELY. Never runs
                               the task's actual code itself.

  2. Redis (the BROKER)     — the queue in the middle. .delay() just writes
                               a message here ("run import_movie_task with
                               title='Dune'") and returns. Same Redis server
                               as our cache, different "drawer" (DB index).

  3. Celery worker process  — a totally separate program you start yourself:
                                   celery -A movie_wishlist worker
                               It watches Redis, pulls jobs off the queue
                               one at a time, and actually RUNS the task
                               function. If this isn't running, jobs just
                               sit in Redis forever — nothing processes them.

FLOW FOR ONE REQUEST:
  view calls import_movie_task.delay("Dune")
      -> message placed on Redis queue                  (instant)
      -> view returns 202 Accepted                       (instant)
      ......(later, independently)......
      -> worker process picks the message off Redis
      -> worker runs the real function body
      -> result (return value) stored back in Redis, if anyone wants to check it

'app' below is THE Celery application object for this whole project — one
instance, imported by every @shared_task and by the worker command.
"""
import os
from celery import Celery

# Tell Celery which settings module to read (same as manage.py does)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_wishlist.settings')

# 'movie_wishlist' = just a name for this Celery app, shown in worker logs
app = Celery('movie_wishlist')

# Read every CELERY_* setting from settings.py (namespace='CELERY' means we
# write CELERY_BROKER_URL there instead of a separate celery-only file).
# This is where 'app' learns WHERE the broker/queue (Redis) lives.
app.config_from_object('django.conf:settings', namespace='CELERY')

# We keep ALL tasks in one central movie_wishlist/tasks.py (not one per app),
# so there's nothing for autodiscover_tasks() to find inside INSTALLED_APPS —
# we just point Celery straight at our one file instead.
app.conf.imports = ('movie_wishlist.tasks',)
