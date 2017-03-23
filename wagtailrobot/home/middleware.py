from __future__ import absolute_import, unicode_literals

from django.utils.deprecation import MiddlewareMixin
from django.utils.translation import ugettext as _

from home.signals import conn


class PageViewMiddleware(MiddlewareMixin):

    def process_template_response(self, request, response):
        try:
            page = response.context_data['self']
        except KeyError:
            return response

        conn.voice.say(_("Do you like your page, {}?").format(page.title))
        return response
