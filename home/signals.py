import qi

from django.utils.functional import cached_property
from django.contrib.auth.signals import user_logged_in, user_logged_out


class NaoConnection(object):
    def __init__(self):
        self.app = qi.Application(url="tcp://koe.local:9559")
        self.app.start()
        self.session = self.app.session

    @cached_property
    def voice(self):
        return self.session.service("ALTextToSpeech")

    def say(self, message, **kwargs):
        return self.voice.say(message, **kwargs)


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
