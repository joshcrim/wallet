import sys
import os

# Add the current wallet directory to python path. Needed for Django
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'wallet'))

# Set Django environment variable to use wallet/settings.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

import django
django.setup()

from .cli import cli

if __name__ == '__main__':
        cli()
