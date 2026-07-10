from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone
from notifications.models import Notification
from .models import Watchlist


"""
We will register this signals file in apps.py of watchlist.
So it automatically invoked/bind with watchlist to receive any signal.
"""

# pre_save = "about to save" — the row is NOT in the database yet.
# So we can still edit fields on the SAME record being saved (here: watched_at),
# and our edit goes into the database together with it. One row, one save.
# Its run to update any specific record if needed.
@receiver(pre_save, sender=Watchlist)
def set_watched_at(sender, instance, **kwargs):
    # Runs just BEFORE saving. If the item is being marked 'watched'
    # and has no watched date yet, stamp the current time automatically.
    if instance.status == 'watched' and instance.watched_at is None:
        instance.watched_at = timezone.now()

# post_save = "already saved" — the watchlist row is safely in the database now.
# Too late to edit it, but perfect for side effects on OTHER tables:
# here we add one new row to the notifications table.
@receiver(post_save, sender=Watchlist)
def notify_on_add(sender, instance, created, **kwargs):
    # Runs just AFTER saving. created=True only for brand new rows,
    # so updates (like a PATCH to change status) don't trigger this.
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f'"{instance.movie.title}" was added to your watchlist',
        )
