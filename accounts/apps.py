from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        # Nothing imports signals.py on its own — this line registers
        # the listeners when Django starts. Without it: no signals, no error.
        import accounts.signals
