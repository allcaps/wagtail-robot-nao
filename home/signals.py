from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from wagtailrobot.behaviour.robotinterface import NaoConnection
conn = NaoConnection()


@receiver(user_logged_in)
def say_hello(sender, user, request, **kwargs):
    name = user.get_full_name()
    if not name:
        name = user.username
    conn.voice.say("Hello {}".format(name))


@receiver(user_logged_out)
def say_goodby(sender, user, request, **kwargs):
    name = user.get_full_name()
    if not name:
        name = user.username
    conn.voice.say("Goodbye {}".format(name))
