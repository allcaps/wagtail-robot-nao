from __future__ import absolute_import, unicode_literals

from .base import *

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gy*2e800xyp#m#l#&jrzc%k@5@f19_^q47)d=9jk^4tev#jspw'


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

NAO_MOCK = False

COMPRESS_ENABLED = True

# LANGUAGE_CODE = 'nl'  # 'en-us' or 'nl' or 'nl-nl'

try:
    from .local import *
except ImportError:
    pass
