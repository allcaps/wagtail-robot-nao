import qi
import time

from django.utils.functional import cached_property

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
        self.app = qi.Application(url="tcp://172.16.0.107:9559")
        self.app.start()
        self.session = self.app.session

    @cached_property
    def voice(self):
        voice = self.session.service("ALTextToSpeech")#pitchShift
        voice.setParameter("pitchShift", 1.0)
        voice.setParameter("speed", 0.5)
        return voice

    @cached_property
    def postureProxy(self):
        alive = self.session.service("ALRobotPosture")
        alive.setBackgroundStrategy('backToNeutral')
        return alive

    @cached_property
    def alive(self):
        return self.session.service("ALAutonomousMoves")

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

    conn = NaoConnection()
    conn.findFaces()

    while True:
        time.sleep(10)
    # conn.voice.say("I got some swag, don't it")
    # for a in ANIMATIONS:
    #     print a
    #     conn.play(a)

if __name__ == '__main__':
    main()
    
