from __future__ import absolute_import, unicode_literals
from thread import start_new_thread

from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext as _

from home.signals import conn


def end_presentation(request):
    conn.voice.say(_("Do you like your page?"))
    conn.voice.say(_("I think it is awesome! LETS PARTY!"))
    conn.voice.say(_("Dear {}... May I have this dance?").format(request.user.get_full_name()))
    #conn.play('User/gangnamstyle-5c4934/gangnam1')
    conn.voice.say(_("That was fun. Thank you very much! Hope to see you soon!"))
    conn.motion.rest()


class PageViewMiddleware(MiddlewareMixin):

    def process_template_response(self, request, response):
        try:
            response.context_data['self']
        except KeyError:
            return response

        start_new_thread(end_presentation, (request,))

        return response
