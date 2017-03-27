from django.apps import apps

from datetime import timedelta
import maya


def parse_date(date):
    date = maya.when(str(date))
    date = date.datetime(to_timezone='US/Eastern').date()

    return date


def generate_payperiods(wallet, date):
    PayPeriod = apps.get_model('transactions', 'PayPeriod')

    payperiod_date = wallet.payperiod_set.filter(current=True).first().date

    payperiods = []
    while payperiod_date < date:
        pp, _ = PayPeriod.objects.get_or_create(
            wallet=wallet,
            date=payperiod_date
        )

        payperiods.append(pp)

        payperiod_date = payperiod_date + timedelta(weeks=2)

    return payperiods


def calculate_payperiod_savings(payperiods):
    savings = 0
    for p in payperiods:
        if p.current is not True:
            savings += p.get_savings()

    return savings
