import os
import sys


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

INSTALLED_APPS = [
    'accounts',
    'transactions',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'thetldb',
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '',
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}
