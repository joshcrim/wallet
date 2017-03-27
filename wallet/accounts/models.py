from django.db import models

from utils import (
    calculate_payperiod_savings,
    generate_payperiods,
    parse_date
)


class User(models.Model):
    username = models.CharField(
        'Username',
        max_length=40,
        unique=True
    )

    def _str__(self):
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

    def get_transactions(self):
        return self.transaction_set.filter(completed=False)

    def update_savings(self, amount):
        self.savings = amount
        self.save()

    def update_payperiod_and_savings(self):
        date = parse_date('today')

        payperiods = generate_payperiods(self, date)
        payperiod_savings = calculate_payperiod_savings(payperiods)

        savings = self.savings + payperiod_savings
        self.update_savings(savings)

        payperiod = payperiods[-1]
        payperiod.current = True
        payperiod.save()

        return payperiod

    def get_payperiod(self, date, commit=False):
        payperiods = generate_payperiods(self, date)
        payperiod = payperiods[-1]

        return payperiod

    def calculate_savings_balance(self, date):
        payperiods = generate_payperiods(self, date)
        savings = calculate_payperiod_savings(payperiods)

        savings = savings + self.savings

        return savings

    def get_upcoming_expenses(self, date):
        date = parse_date(date)
        payperiods = self.payperiod_set.filter(date__gt=date)

        expenses = []
        total_expenses = 0
        for payperiod in payperiods:
            occurrences = payperiod.occurrence_set.filter(transaction__completed=True)

            if occurrences.exists():
                for occurrence in occurrences:
                    expenses.append(
                        [payperiod.date, occurrence.transaction.name, occurrence.amount]
                    )

                    total_expenses += occurrence.amount

        return expenses, total_expenses
