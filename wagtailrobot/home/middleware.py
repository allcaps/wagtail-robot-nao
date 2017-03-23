from __future__ import absolute_import, unicode_literals

import time
from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext as _

from home.signals import conn


class PageViewMiddleware(MiddlewareMixin):

    def process_template_response(self, request, response):
        try:
            page = response.context_data['self']
        except KeyError:
            return response

        conn.voice.say(_("Do you like your page?"))
        conn.voice.say(_("I think it is awesome! LETS PARTY!"))
        conn.voice.say(_("Dear {}... May I have this dance?".format(request.user.get_full_name())))
        conn.play('User/gangnamstyle-5c4934/gangnam1')
        conn.voice.say(_("That was fun. Thank you very much! Hope to see you soon!"))

        return response

