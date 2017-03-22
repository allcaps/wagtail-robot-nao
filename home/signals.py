from django.contrib.auth.signals import user_logged_in, user_logged_out

from wagtailrobot.behaviour.robotinterface import NaoConnection
conn = NaoConnection()


def say_hello(sender, user, request, **kwargs):
    name = user.get_full_name()
    if not name:
        name = user.username
    conn.voice.say("Hello {}".format(name))


def say_goodby(sender, user, request, **kwargs):
    name = user.get_full_name()
    if not name:
        name = user.username
    conn.voice.say("Goodbye {}".format(name))


user_logged_in.connect(say_hello)
user_logged_out.connect(say_goodby)
