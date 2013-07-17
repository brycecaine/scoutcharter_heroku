# Django production settings for scoutcharter project.

try:
    from scoutcharter.settings_local import *

except ImportError, e:
    print 'Unable to load settings_local.py:', e

DEBUG = True # For now; but change this to False when live

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'deqlp570vcobof',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'szkgmhjuigtjic',
        'PASSWORD': 'W3CPrXJ0ked_GEjhbJpHv0SMeM',
        'HOST': 'ec2-54-227-252-82.compute-1.amazonaws.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '5432',                      # Set to empty string for default.
    }
}

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(PROJECT_ROOT,'./')
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static/')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

TEMPLATE_CONTEXT_PROCESSORS = ('django.contrib.auth.context_processors.auth',
                               'django.core.context_processors.debug',
                               'django.core.context_processors.i18n',
                               'django.core.context_processors.media',
                               'django.core.context_processors.static',
                               'django.core.context_processors.tz',
                               'django.contrib.messages.context_processors.messages')
