import click
import crayons

from decimal import Decimal

from utils import echo
from utils import parse

from transactions.models import Occurrence, Transaction


def add_transaction(account, trans_type):
    if trans_type is 'Income':
        trans_int = 0
    elif trans_type is 'Expense':
        trans_int = 1

    transaction = Transaction(
        wallet=account.wallet,
        trans_type=trans_int,
    )

    transaction.name = click.prompt(crayons.magenta('{0} Name'.format(trans_type)), type=str)
    transaction.amount = click.prompt(crayons.magenta('{0} Amount'.format(trans_type)), type=Decimal)

    recurring = click.prompt(
        crayons.magenta('Is this One Time(0) or Recurring(1)'),
        type=click.Choice(['0', '1'])
    )

    if recurring is '1':
        transaction.frequency = click.prompt(
            crayons.magenta('BiWeekly(0) or Monthly(1)'), type=int
        )
        transaction.save()

    else:
        transaction.frequency = 0
        transaction.completed = True
        transaction.save()

        date = click.prompt(crayons.magenta('Date occurs'), type=str)
        date = parse.date(date)

        payperiod = account.wallet.get_payperiod(date)

        occurrence = Occurrence(
            payperiod=payperiod,
            transaction=transaction,
            amount=transaction.amount
        )

        occurrence.save()

    echo.yellow(
        "{0} created: {1} ${2}",
        trans_type, transaction.name, transaction.amount
    )


def edit_transaction(account, trans_type):
    if trans_type is 'Income':
        occurrences = account.incomes
    elif trans_type is 'Expense':
        occurrences = account.expenses

    echo.cyan(
        "{0}: ${0}",
        trans_type, account.expense_total
    )

    echo.transactions(occurrences)
    echo.newline()

    choices = [occurrence.name for occurrence in occurrences]
    transaction_name = click.prompt(
        crayons.magenta('Name of transaction to edit'),
        type=click.Choice(choices)
    )

    occurrence = occurrences.filter(
        transaction__name=transaction_name
    ).first()

    editable = click.prompt(
        crayons.magenta('Edit name(0) or amount(1)'),
        type=click.Choice(['0', '1'])
    )

    if editable is '0':
        new_name = click.prompt(crayons.magenta('New Name'), type=str)

        occurrence.transaction.name = new_name
        occurrence.transaction.save()

    elif editable is '1':
        payperiod_or_forever = click.prompt(
            crayons.magenta(
                'Edit for this payperiod(0) or forever(1):'
            ),
            type=click.Choice(['0', '1'])
        )

        new_amount = click.prompt(crayons.magenta('New Amount'), type=Decimal)

        if payperiod_or_forever is '0':
            occurrence.amount = new_amount
            occurrence.save()

        elif payperiod_or_forever is '1':
            occurrence.amount = new_amount
            occurrence.save()

            occurrence.transaction.amount = new_amount
            occurrence.transaction.save()

    echo.yellow(
        "{0} Edited. {1}: {2}",
        trans_type, occurrence.name, occurrence.amount
    )


def delete_transaction(account, trans_type):
    if trans_type is 'Income':
        occurrences = account.incomes
    elif trans_type is 'Expense':
        occurrences = account.expenses

    echo.cyan(
        "{0}: ${0}",
        trans_type, account.expense_total
    )

    echo.transactions(occurrences)
    echo.newline()

    choices = [occurrence.name for occurrence in occurrences]
    transaction_name = click.prompt(
        crayons.magenta('Name of transaction to delete'),
        type=click.Choice(choices)
    )

    occurrence = occurrences.filter(
        transaction__name=transaction_name
    ).first()

    payperiod_or_forever = click.prompt(
        crayons.magenta(
            'Delete for this payperiod(0) or forever(1):'
        ),
        type=click.Choice(['0', '1'])
    )

    if payperiod_or_forever is '0':
        occurrence.delete()

    elif payperiod_or_forever is '1':
        occurrence.transaction.delete()

    echo.yellow(
        "{0} Deleted. {1}: {2}",
        trans_type, occurrence.name, occurrence.amount
    )
