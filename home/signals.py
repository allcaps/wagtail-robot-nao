from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.wagtailcore.signals import page_published
from wagtail.wagtailimages.models import Image
from wagtailrobot.behaviour.robotinterface import NaoConnection

from .models import HomePage

conn = NaoConnection()


@receiver(user_logged_in)
def say_hello(sender, user, request, **kwargs):
    name = user.get_full_name()
    if not name:
        name = user.username
    conn.voice.say("Hello {}".format(name))
    conn.play("animations/Sit/Emotions/Neutral/AskForAttention_1")
    conn.findFaces()
    img = conn.takePicturePNG(name)
    image = Image(file=img, title=name)
    image.save()
    conn.stopFindingFaces()
    conn.voice.say("Now that you are logged in, please create a page.")


@receiver(user_logged_out)
def say_goodby(sender, user, request, **kwargs):
    name = user.get_full_name()
    if not name:
        name = user.username
    conn.voice.say("Goodbye {}".format(name))


@receiver(post_save, sender=HomePage)
def not_live(sender, instance, **kwargs):
    if not instance.live:
        conn.voice.say("Nice, but your page is not published yet!")


@receiver(page_published)
def say_stupid(sender, instance, revision, **kwargs):
    title = instance.title
    word = 'cool'
    if 'page' in title or 'title' in title:
        word = 'stupid'
        conn.play('animations/Stand/Emotions/Negative/Angry_1')
    conn.voice.say("{} is a {} title for a page".format(title, word))


@receiver(user_login_failed)
def give_password_hint(*args, **kwargs):
    conn.voice.say("1? 2? 3? Is really your password? That can't be secure! Try: 1, 2, 3, 4!")
