import qi

from django.utils.functional import cached_property

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


def main():

    conn = NaoConnection()
    conn.voice.say("Laurens are your head and face mixed up")


if __name__ == '__main__':
    main()