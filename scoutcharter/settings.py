# Django production settings for scoutcharter project.

try:
    from scoutcharter.settings_local import *

except ImportError, e:
    print 'Unable to load settings_local.py:', e

DEBUG = True # For now; but change this to False when live

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'd9279msvqqglg3',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'jfnebpdiqntvli',
        'PASSWORD': 'kcoLlLvLJTo0Ju3B3twgDyDhAs',
        'HOST': 'ec2-54-225-123-71.compute-1.amazonaws.com',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
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

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
            os.path.join(BASE_DIR, 'static'),
            )
