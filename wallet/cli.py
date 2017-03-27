import click
import crayons
from decimal import Decimal

import sys

from utils import parse_date

from accounts.models import Wallet
from transactions.models import Occurrence, Transaction


class Account(object):
    def __init__(self, date=None):
        # Get wallet and update current payperiod and savings balance
        self.wallet = Wallet.objects.first()
        self.wallet.update_payperiod_and_savings()

        # Get the payperiod for the requested date or today
        date = date or 'today'
        self.date = parse_date(date)

        today = parse_date('today')

        if self.date < today:
            click.echo(crayons.red("Select a date of today or later."))
            sys.exit()

        self.payperiod = self.wallet.get_payperiod(self.date)

        # Run payperiod Calculations
        self.incomes, self.income_total = self.payperiod.get_incomes()
        self.expenses, self.expense_total = self.payperiod.get_expenses()
        self.upcoming, self.upcoming_total = self.wallet.get_upcoming_expenses(self.date)


@click.group(invoke_without_command=True)
@click.argument('date', required=False, nargs=-1)
@click.option(
    '--help', '-h',
    is_flag=True,
    default=None,
    help="Show this message then exit."
)
@click.option('--setsavings')
@click.option('--edit', nargs=1)
@click.pass_context
def cli(ctx, date=None, edit=None, setsavings=None, help=False):

    account = ctx.obj = Account(date=date)

    options = {
        'income': income,
        'expenses': expense,
    }

    if setsavings:
        savings = setsavings
        account.wallet.savings = savings
        account.wallet.save()

        click.echo(
            crayons.yellow("New savings balance: {0}".format(account.wallet.savings))
        )

    elif edit:
        if edit not in options:
            click.echo(crayons.red('Enter a valid command'))
            sys.exit()

        ctx.invoke(options[edit])

    else:
        click.echo('\n', nl=False)

        click.echo(
            crayons.cyan("Wallet for {0} on {1}".format(
                account.wallet, account.date.strftime("%B %d, %Y"))
            )
        )
        click.echo(
            crayons.yellow("Savings balance: \t${0}".format(
                account.wallet.calculate_savings_balance(account.date)))
        )
        click.echo(
            crayons.yellow("PayPeriod Savings: \t${0}".format(
                account.payperiod.get_savings()))
        )
        click.echo('\n', nl=False)

        click.echo(crayons.cyan("Income: ${0}".format(account.income_total)))
        for trans in account.incomes:
            if len(trans.transaction.name) <= 5:
                click.echo(
                    crayons.yellow("\t\t{0}:\t${1}".format(
                        trans.transaction.name, trans.amount)
                    )
                )
            else:
                click.echo(
                    crayons.yellow("\t{0}:\t${1}".format(
                        trans.transaction.name, trans.amount)
                    )
                )
        click.echo('\n', nl=False)

        click.echo(crayons.cyan("Expenses: ${0}".format(account.expense_total)))
        for trans in account.expenses:
            if len(trans.transaction.name) <= 5:
                click.echo(
                    crayons.yellow("\t{0}:\t\t${1}".format(
                        trans.transaction.name, trans.amount)
                    )
                )
            else:
                click.echo(
                    crayons.yellow("\t{0}:\t${1}".format(
                        trans.transaction.name, trans.amount)
                    )
                )
        click.echo('\n', nl=False)

        click.echo(crayons.cyan("Upcoming Expenses: ${0}".format(account.upcoming_total)))
        for trans in account.upcoming:
            click.echo(crayons.blue('\t{0}'.format(trans[0].strftime("%B %d, %Y"))))

            if len(trans[1]) <= 5:
                click.echo(
                    crayons.yellow("\t{0}:\t\t${1}".format(trans[1], trans[2]))
                )
            else:
                click.echo(
                    crayons.yellow("\t{0}:\t${1}".format(trans[1], trans[2]))
                )
        click.echo('\n', nl=False)


@click.command(help="View and modify savings balance.")
@click.pass_obj
def savings(account):
    savings = click.prompt(crayons.magenta('New savings balance'))
    account.wallet.savings = savings
    account.wallet.save()

    click.echo(
        crayons.yellow("New savings balance: {0}".format(account.wallet.savings))
    )


@click.command(help="List and modify incomes.")
@click.pass_obj
def income(account):

    income = Transaction(
        wallet=account.wallet,
        trans_type=0,
    )

    income.name = click.prompt(crayons.magenta('Income Name', type=str), type=str)
    income.amount = click.prompt(crayons.magenta('Income Amount'), type=Decimal)

    recurring = click.prompt(crayons.magenta('Is this a One Time(0) or Recurring(1) income'), type=int)

    if recurring:
        income.frequency = click.prompt(crayons.magenta('BiWeekly(0) or Monthly(1)'), type=int)
        income.save()

    else:
        income.frequency = 0
        income.completed = True
        income.save()

        date = click.prompt(crayons.magenta('Date income occurs'), type=str)
        date = parse_date(date)

        payperiod = account.wallet.get_payperiod(date)

        occurrence = Occurrence(
            payperiod=payperiod,
            transaction=income,
            amount=income.amount
        )

        occurrence.save()

    click.echo(
        crayons.yellow("Income created: {0} ${1}".format(income.name, income.amount))
    )


@click.command(help="List and modify expenses.")
@click.pass_obj
def expense(account):
    expense = Transaction(
        wallet=account.wallet,
        trans_type=1,
    )

    expense.name = click.prompt(crayons.magenta('Expense Name'), type=str)
    expense.amount = click.prompt(crayons.magenta('Expense Amount'), type=Decimal)

    recurring = click.prompt(crayons.magenta('Is this a One Time(0) or Recurring(1) expense'), type=int)

    if recurring:
        expense.frequency = click.prompt(crayons.magenta('BiWeekly(0) or Monthly(1)'), type=int)
        expense.save()

    else:
        expense.frequency = 0
        expense.completed = True
        expense.save()

        date = click.prompt(crayons.magenta('Date expense occurs'), type=str)
        date = parse_date(date)

        payperiod = account.wallet.get_payperiod(date)

        occurrence = Occurrence(
            payperiod=payperiod,
            transaction=expense,
            amount=expense.amount
        )

        occurrence.save()

    click.echo(
        crayons.yellow("Expense created: {0} ${1}".format(expense.name, expense.amount))
    )


cli.add_command(savings)
cli.add_command(income)
cli.add_command(expense)


if __name__ == '__main__':
    cli()
