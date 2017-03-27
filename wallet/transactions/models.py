from django.db import models
from django.db.models import Sum
from django.utils import timezone


class Transaction(models.Model):
    INCOME, EXPENSE = range(2)
    trans_types = (
        (INCOME, 'Income'),
        (EXPENSE, 'Expense'))

    BIWEEKLY, MONTHLY = range(2)
    frequencies = (
        (BIWEEKLY, 'BiWeekly'),
        (MONTHLY, 'Monthly')
    )

    wallet = models.ForeignKey('accounts.Wallet')
    name = models.CharField(max_length=40)
    trans_type = models.IntegerField(choices=trans_types)
    frequency = models.IntegerField(choices=frequencies)
    amount = models.DecimalField(decimal_places=2, max_digits=7)
    completed = models.BooleanField(default=False, blank=True)

    class Meta:
        unique_together = (('wallet', 'name'),)

    def __str__(self):
        return '%s' % self.name


class Occurrence(models.Model):
    payperiod = models.ForeignKey('transactions.PayPeriod')
    transaction = models.ForeignKey('transactions.Transaction')
    amount = models.DecimalField(decimal_places=2, max_digits=7)

    def __str__(self):
        return '%s' % self.transaction.name


class PayPeriod(models.Model):
    wallet = models.ForeignKey('accounts.Wallet')
    date = models.DateField(default=timezone.now())
    current = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'PayPeriod'

    def __str__(self):
        return 'PayPeriod: %s' % self.date

    def _generate_occurrences(self):
        transactions = self.wallet.get_transactions()
        occurrences = self.occurrence_set.all()

        occurrence_list = [
            Occurrence(
                transaction=transaction,
                payperiod=self,
                amount=transaction.amount
            )
            for transaction in transactions
            if not occurrences.filter(transaction=transaction)
        ]

        for occurrence in occurrence_list:
            if occurrence.transaction.frequency is 1:
                occurrence.amount = occurrence.amount / 2

        Occurrence.objects.bulk_create(occurrence_list)

        return self.occurrence_set.order_by('transaction__name', 'amount')

    def get_incomes(self):
        incomes = self._generate_occurrences().filter(transaction__trans_type=0)
        income_total = incomes.aggregate(total=Sum('amount'))['total']

        return incomes, income_total

    def get_expenses(self):
        expenses = self._generate_occurrences().filter(transaction__trans_type=1)
        expense_total = expenses.aggregate(total=Sum('amount'))['total']

        return expenses, expense_total

    def get_savings(self):
        _, income_total = self.get_incomes()
        _, expense_total = self.get_expenses()

        payperiod_savings = income_total - expense_total

        return payperiod_savings

    def save(self, *args, **kwargs):
        if self.current:
            PayPeriod.objects.filter(
                wallet=self.wallet).exclude(id=self.id).update(current=False)

        super(PayPeriod, self).save(*args, **kwargs)
