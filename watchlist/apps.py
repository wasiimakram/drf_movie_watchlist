from django.apps import AppConfig


class WatchlistConfig(AppConfig):
    name = 'watchlist'

    def ready(self):
        # Nothing imports signals.py on its own — this line registers
        # the listeners when Django starts. Without it: no signals, no error.
        import watchlist.signals
