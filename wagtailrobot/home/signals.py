from thread import start_new_thread
from django.conf import settings
from django.contrib.auth.signals import (
    user_logged_in,
    user_logged_out,
    user_login_failed,
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from wagtail.wagtailcore.signals import page_published
from wagtailrobot.behaviour.robotinterface import NaoConnection

from .models import Page

conn = NaoConnection()

if 'nl' in settings.LANGUAGE_CODE:
    conn.voice.setLanguage('Dutch')
else:
    conn.voice.setLanguage('English')


@receiver(user_logged_in)
def say_hello(sender, user, request, **kwargs):
    conn.findFaces()
    name = user.get_full_name()
    if not name:
        name = user.username
    conn.voice.say(_("Hello {name}").format(name=name))
    start_new_thread(conn.voice.say, (_("Create a page: Add a title, image and click \\emph=2\\ 'Save draft'."),))


@receiver(user_logged_out)
def say_goodby(sender, user, request, **kwargs):
    name = user.get_full_name()
    if not name:
        name = user.username
    conn.voice.say(_("Goodbye {name}").format(name=name))


@receiver(post_save, sender=Page)
def not_live(sender, instance, **kwargs):
    if (instance.revisions.count() == 1 and not instance.live) or \
       (instance.live and instance.has_unpublished_changes):
        conn.voice.say(_("Nice, but your page is not published yet!"))


@receiver(page_published)
def give_comment_on_page_title(sender, instance, revision, **kwargs):
    title = instance.title
    adjective = _("cool")
    if _("page") in title or _("title") in title:
        adjective = _("stupid")
        start_new_thread(conn.playAsync, ("animations/Stand/Emotions/Negative/Angry_1",))
    conn.voice.say(_("{title} is a {adjective} title for a page").format(title=title, adjective=adjective))
    conn.voice.say(_("Your page is now published. It is the top item in the list. View it by clicking \\pau=1\\ \\emph=3\\ live. The live button is in the status column."))


@receiver(user_login_failed)
def give_password_hint(*args, **kwargs):
    conn.findFaces()
    name = kwargs['credentials']['username']
    start_new_thread(conn.asyncTakePicturePNG, (name,))
    conn.voice.say(_("1? 2? 3? Is really your password? That can't be secure! Try: 1. 2. 3. \\pau=2\\ \\emph=2\\ 4!"))
