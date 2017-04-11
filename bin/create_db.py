# -- Set up Django environment -- #

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'wallet'))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallet.settings")

import django
django.setup()

# ------------------------------- #

from datetime import date

from accounts.models import User, Wallet
from transactions.models import PayPeriod, Transaction


payperiod_date = date(2017, 3, 3)

user, _ = User.objects.get_or_create(
    username='jshcrm'
)

wallet, _ = Wallet.objects.get_or_create(
    user=user,
    defaults={'savings': 6360.00}
)

PayPeriod.objects.get_or_create(
    wallet=wallet,
    defaults={
        'date':payperiod_date,
        'current':True
    }
)

Transaction.objects.get_or_create(
    name='Paycheck',
    defaults={
        'wallet': wallet,
        'trans_type': 0,
        'amount': 3000.00,
        'frequency': 0
    })

Transaction.objects.get_or_create(
    name='Rent',
    defaults={
        'wallet': wallet,
        'trans_type': 1,
        'amount': 600.00,
        'frequency': 1
    }
)

Transaction.objects.get_or_create(
    name='Cell Phone',
    defaults={
        'wallet': wallet,
        'trans_type': 1,
        'amount': 120.00,
        'frequency': 1
    }
)

Transaction.objects.get_or_create(
    name='Car Insurance',
    defaults={
        'wallet': wallet,
        'trans_type': 1,
        'amount': 70.00,
        'frequency': 1
    }
)

Transaction.objects.get_or_create(
    name='Groceries',
    defaults={
        'wallet': wallet,
        'trans_type': 1,
        'amount': 120.00,
        'frequency': 0
    }
)

Transaction.objects.get_or_create(
    name='Gas',
    defaults={
        'wallet': wallet,
        'trans_type': 1,
        'amount': 50.00,
        'frequency': 0
    }
)

Transaction.objects.get_or_create(
    name='Spending',
    defaults={
        'wallet': wallet,
        'trans_type': 1,
        'amount': 200.00,
        'frequency': 0
    }
)

Transaction.objects.get_or_create(
    name='Cigs',
    defaults={
        'wallet': wallet,
        'trans_type': 1,
        'amount': 20.00,
        'frequency': 0
    }
)

Transaction.objects.get_or_create(
    name='Dog Food',
    defaults={
        'wallet': wallet,
        'trans_type': 1,
        'amount': 30.00,
        'frequency': 0
    }
)
