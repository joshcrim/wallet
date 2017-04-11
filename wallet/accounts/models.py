from django.apps import apps
from django.db import models

from collections import namedtuple
from datetime import timedelta

from utils import parse


class User(models.Model):
    username = models.CharField(
        'Username',
        max_length=40,
        unique=True
    )

    def __str__(self):
        return self.username


class Wallet(models.Model):

    user = models.OneToOneField('accounts.User')
    savings = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        default=0.00
    )

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'

    def __str__(self):
        return '{0}'.format(self.user.username)

    @staticmethod
    def calculate_payperiod_savings(payperiods):
        savings = 0
        for p in payperiods:
            if p.current is not True:
                savings += p.get_savings()

        return savings

    def generate_payperiods(self, date):
        PayPeriod = apps.get_model('transactions', 'PayPeriod')

        payperiod_date = self.payperiod_set.filter(current=True).first().date

        payperiods = []
        while payperiod_date <= date:
            pp, _ = PayPeriod.objects.get_or_create(
                wallet=self,
                date=payperiod_date
            )

            payperiods.append(pp)

            payperiod_date = payperiod_date + timedelta(weeks=2)

        return payperiods

    def get_transactions(self):
        return self.transaction_set.filter(completed=False)

    def update_savings(self, amount):
        self.savings = amount
        self.save()

    def update_payperiod_and_savings(self):
        date = parse.date('today')

        payperiods = self.generate_payperiods(date)
        payperiod_savings = self.calculate_payperiod_savings(payperiods)

        savings = self.savings + payperiod_savings
        self.update_savings(savings)

        payperiod = payperiods[-1]
        payperiod.current = True
        payperiod.save()

        return payperiod

    def get_payperiod(self, date):
        payperiods = self.generate_payperiods(date)
        payperiod = payperiods[-1]

        return payperiod

    def calculate_savings_balance(self, date):
        payperiods = self.generate_payperiods(date)
        savings = self.calculate_payperiod_savings(payperiods)

        savings = savings + self.savings

        return savings

    def get_upcoming_expenses(self, date):
        date = parse.date(date)
        payperiods = self.payperiod_set.filter(date__gt=date)

        Expense = namedtuple('Expenses', ['date', 'name', 'amount'])

        expenses = []
        total_expenses = 0
        for payperiod in payperiods:
            occurrences = payperiod.occurrence_set.filter(transaction__completed=True)

            if occurrences.exists():
                for occurrence in occurrences:
                    expenses.append(
                        Expense(payperiod.date, occurrence.name, occurrence.amount)
                    )

                    total_expenses += occurrence.amount

        return expenses, total_expenses
