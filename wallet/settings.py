import os

ROOT = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

INSTALLED_APPS = [
    'accounts',
    'transactions',
    'utils'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT, 'mydatabase')
    }
}
