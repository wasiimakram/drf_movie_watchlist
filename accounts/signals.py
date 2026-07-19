from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


@receiver(post_save, sender=User)
def send_email_on_register(sender, instance, created, **kwargs):
    # Only NEW + INACTIVE accounts (the register flow sets is_active=False).
    # createsuperuser makes active users -> no email for those.
    if created and not instance.is_active:

        # The activation link must say WHICH user to activate — but putting a
        # raw id in a URL invites guessing (/activate/7/ -> try /activate/8/).
        # So the link carries TWO parts: an encoded id + a secret token.

        # Part 1: the user's id, made URL-safe.
        # force_bytes(7) turns the id into bytes (b'7') because the encoder
        # needs bytes; urlsafe_base64_encode turns those bytes into text that
        # can live in a URL, e.g. 'Nw'. NOT encryption — just safe packaging.
        uid = urlsafe_base64_encode(force_bytes(instance.pk))

        # Part 2: the secret. Django builds a signed hash from things only the
        # server knows (SECRET_KEY + this user's password hash + last login).
        # It can't be guessed, and it EXPIRES on its own: activating changes
        # the user's state, which changes the hash -> old token stops working.
        # No token table in the DB needed — the math IS the storage.
        token = default_token_generator.make_token(instance)

        # Glue both into the URL our activate endpoint will receive:
        # http://127.0.0.1:8000/api/auth/activate/Nw/cx8a2b-.../
        link = f'{settings.SITE_URL}/api/auth/activate/{uid}/{token}/'

        # Fill the HTML template with this user's values.
        # render_to_string = "render the template, but give me the result as a
        # string instead of sending it to a browser". The dict is the template
        # context: {{ username }} and {{ activation_link }} get replaced.
        html = render_to_string('emails/activation.html', {
            'username': instance.username,
            'activation_link': link,
        })

        # Actually send. With the console backend this prints to the runserver
        # terminal instead of really emailing — perfect for development.
        send_mail(
            'Activate your account',           # subject line
            f'Activate here: {link}',          # plain-text body (fallback for clients that block HTML)
            settings.DEFAULT_FROM_EMAIL,       # sender address (from settings.py)
            [instance.email],                  # recipient LIST — could be several
            html_message=html,                 # the pretty HTML version, used when the client allows it
        )
