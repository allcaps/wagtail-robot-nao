import io
import qi
import time
import vision_definitions

from django.conf import settings
from django.core.files.images import ImageFile
from django.utils.functional import cached_property
from django.utils.six import BytesIO
from mock import MagicMock
from PIL import Image

ANIMATIONS = [
    "animations/Stand/Emotions/Negative/Angry_1",
    "animations/Stand/Emotions/Negative/Anxious_1",
    "animations/Stand/Emotions/Negative/Bored_2",
    "animations/Stand/Emotions/Negative/Disappointed_1",
    "animations/Stand/Emotions/Negative/Exhausted_2",
    "animations/Stand/Emotions/Negative/Fearful_1",
    "animations/Stand/Emotions/Negative/Sad_1",
    "animations/Stand/Emotions/Negative/Sorry_1",
    "animations/Stand/Emotions/Negative/Surprise_2",
    "animations/Stand/Emotions/Neutral/AskForAttention_1",
    "animations/Stand/Emotions/Neutral/Confused_1",
    "animations/Stand/Emotions/Neutral/Determined_1",
    "animations/Stand/Emotions/Neutral/Hello_1",
    "animations/Stand/Emotions/Positive/Amused_1",
    "animations/Stand/Emotions/Positive/Enthusiastic_1",
    "animations/Stand/Emotions/Positive/Excited_2",
    "animations/Stand/Emotions/Positive/Happy_2",
    "animations/Stand/Emotions/Positive/Hysterical_1",
    "animations/Stand/Emotions/Positive/Interested_1",
    "animations/Stand/Emotions/Positive/Laugh_1",
    "animations/Stand/Emotions/Positive/Proud_1",
    "animations/Stand/Emotions/Positive/Relieved_1",
    "animations/Stand/Emotions/Positive/Shy_1",
    "animations/Stand/Emotions/Positive/Sure_1",
    "animations/Stand/Emotions/Positive/Winner_1",
    "animations/Stand/Gestures/Angry_1",
    "animations/Stand/Gestures/Applause_1",
    "animations/Stand/Gestures/No_1",
    "animations/Stand/Gestures/Yes_2",
    "animations/Stand/Reactions/SeeSomething_4",
    "animations/Stand/Reactions/TouchHead_1",
    "animations/Stand/Waiting/LoveYou_1",
    "animations/Stand/Waiting/Think_1",
    "animations/Sit/BodyTalk/Listening/Listening_1",
    "animations/Sit/BodyTalk/Thinking/Remember_1",
    "animations/Sit/Emotions/Negative/Angry_1",
    "animations/Sit/Emotions/Negative/Fear_1",
    "animations/Sit/Emotions/Negative/Sad_1",
    "animations/Sit/Emotions/Negative/Surprise_1",
    "animations/Sit/Emotions/Neutral/AskForAttention_1",
    "animations/Sit/Emotions/Neutral/Sneeze_1",
    "animations/Sit/Emotions/Positive/Happy_1",
    "animations/Sit/Emotions/Positive/Hungry_1",
    "animations/Sit/Emotions/Positive/Laugh_1",
    "animations/Sit/Emotions/Positive/Shy_1",
    "animations/Sit/Emotions/Positive/Winner_1",
    "animations/Sit/Gestures/ComeOn_1",
    "animations/Sit/Reactions/Heat_1",
    "animations/Sit/Reactions/LightShine_1",
    "animations/Sit/Reactions/TouchHead_3",
    "animations/Sit/Waiting/Bored_1"
]


class NaoConnection(object):
    def __init__(self):
        if getattr(settings, "NAO_MOCK", False):
            self.app = MagicMock()
        else:
            self.app = qi.Application(url="tcp://172.16.0.107:9559")
        self.app.start()
        self.session = self.app.session

    @cached_property
    def voice(self):
        voice = self.session.service("ALTextToSpeech")#pitchShift
        voice.setParameter("pitchShift", 1.0)
        voice.setParameter("speed", 100)
        return voice

    @cached_property
    def postureProxy(self):
        return self.session.service("ALRobotPosture")

    @cached_property
    def alive(self):
        alive = self.session.service("ALAutonomousMoves")
        alive.setBackgroundStrategy('backToNeutral')
        return alive

    @cached_property
    def selfaware(self):
        return self.session.service("ALBasicAwareness")

    @cached_property
    def motion(self):
        return self.session.service("ALMotion")

    def findFaces(self):
        self.motion.wakeUp()
        if not self.selfaware.isAwarenessRunning():
            self.selfaware.startAwareness()
        if not self.alive.getExpressiveListeningEnabled():
            self.alive.setExpressiveListeningEnabled(True)

    def stop(self):
        if self.animation.getRunningBehaviors():
            self.animation.stopAllBehaviors()
        self.stopFindingFaces()

    def stopFindingFaces(self):
        if self.selfaware.isAwarenessRunning():
            self.selfaware.stopAwareness()
        if self.alive.getExpressiveListeningEnabled():
            self.alive.setExpressiveListeningEnabled(False)

    @cached_property
    def camera(self):
        return self.session.service("ALVideoDevice")

    def takePicturePNG(self, name):
        resolution = vision_definitions.k4VGA
        colorSpace = vision_definitions.kRGBColorSpace
        fps = 5
        nameId = self.camera.subscribe("python_GVM", resolution, colorSpace, fps)
        pic = self.camera.getImageRemote(nameId)
        self.camera.unsubscribe(nameId)
        imageWidth = pic[0]
        imageHeight = pic[1]
        array = pic[6]
        f = BytesIO()

        # Create a PIL Image from our pixel array.
        im = Image.frombytes("RGB", (imageWidth, imageHeight), str(array))

        # Save the image.
        im.save(f, "PNG")
        return ImageFile(f, name='{}.png'.format(name))

    @cached_property
    def animation(self):
        return self.session.service("ALBehaviorManager")

    def play(self, name):
        posture = self.postureProxy.getPosture()
        if name.startswith("animations/Stand/") and not "Stand" in posture:
            self.postureProxy.goToPosture("Stand", 1.0)
        elif name.startswith("animations/Sit/") and not "Sit" in posture:
            self.postureProxy.goToPosture("Sit", 1.0)
        self.animation.runBehavior(name)

    def say(self, message, **kwargs):
        return self.voice.say(message, **kwargs)


def main():
    try:
        conn = NaoConnection()
        conn.findFaces()
        conn.alive
        conn.voice.say("I got some \\pau=1\\ \\emph=2\\ \\vol=150\\swag, \\vol=100\\\\emph=0\\\\rspd=50\\don't it \\emph=2\\bieaahtch")
        conn.takePicturePNG('henk.png')
        print "jjkh"
        # for a in ANIMATIONS:
        #     print a
        #     conn.play(a)

        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        conn.stop()

if __name__ == '__main__':
    main()
