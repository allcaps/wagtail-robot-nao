import qi

from django.utils.functional import cached_property

class NaoConnection(object):
    def __init__(self):
        self.app = qi.Application(url="tcp://172.16.0.107:9559")
        self.app.start()
        self.session = self.app.session

    @cached_property
    def voice(self):
        voice = self.session.service("ALTextToSpeech")#pitchShift
        voice.setParameter("pitchShift", 1.0)
        voice.setParameter("speed", 0.5)
        return voice

    def say(self, message, **kwargs):
        return self.voice.say(message, **kwargs)


def main():

    conn = NaoConnection()
    conn.voice.say("Laurens are your head and face mixed up")


if __name__ == '__main__':
    main()