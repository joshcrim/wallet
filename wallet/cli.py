import click
import sys

from utils import echo
from utils import prompt
from utils import parse

from accounts.models import Wallet


class Account(object):
    def __init__(self, date=None):
        # Get wallet and update current payperiod and savings balance
        self.wallet = Wallet.objects.first()
        self.wallet.update_payperiod_and_savings()

        # Get the payperiod for the requested date or today
        date = date or 'today'
        self.date = parse.date(date)

        today = parse.date('today')

        if self.date < today:
            echo.red("Select a date of today or later.")
            sys.exit()

        self.payperiod = self.wallet.get_payperiod(self.date)

        # Run payperiod Calculations
        self.incomes, self.income_total = self.payperiod.get_incomes()
        self.expenses, self.expense_total = self.payperiod.get_expenses()
        self.upcoming, self.upcoming_total = self.wallet.get_upcoming_expenses(self.date)


@click.group(invoke_without_command=True)
@click.argument('date', required=False, nargs=-1)
@click.option('--setsavings')
@click.option('--add', type=click.Choice(['income', 'expense']))
@click.option('--edit', type=click.Choice(['income', 'expense']))
@click.option('--delete', type=click.Choice(['income', 'expense']))
@click.pass_context
def cli(ctx, date=None, setsavings=None, add=None, edit=None, delete=None):

    account = ctx.obj = Account(date=date)

    options = {
        'income': income,
        'expense': expense,
    }

    if setsavings:
        account.wallet.update_savings(setsavings)

        echo.yellow("New savings balance: {0}", account.wallet.savings)

    elif add:
        account.context = 'add'
        ctx.invoke(options[add])

    elif edit:
        account.context = 'edit'
        ctx.invoke(options[edit])

    elif delete:
        account.context = 'delete'
        ctx.invoke(options[delete])

    else:
        echo.newline()

        echo.cyan(
            "Wallet for {0} on {1}",
            account.wallet,
            account.date.strftime("%B %d, %Y")
        )

        echo.yellow(
            "Savings balance: \t${0}",
            account.wallet.calculate_savings_balance(account.date)
        )

        echo.yellow(
            "PayPeriod Savings: \t${0}",
            account.payperiod.get_savings()
        )

        echo.newline()

        echo.cyan("Income: ${0}", account.income_total)
        echo.transactions(account.incomes)

        echo.newline()

        echo.cyan("Expenses: ${0}", account.expense_total)
        echo.transactions(account.expenses)

        echo.newline()

        echo.cyan("Upcoming Expenses: ${0}", account.upcoming_total)
        echo.transactions(account.upcoming)

        echo.newline()


@click.command(help="List and modify incomes.")
@click.pass_obj
def income(account):

    if account.context is 'add':
        prompt.add_transaction(account, 'Income')
        echo.newline()

    elif account.context is 'edit':
        prompt.edit_transaction(account, 'Income')
        echo.newline()

    elif account.context is 'delete':
        prompt.delete_transaction(account, 'Income')
        echo.newline()


@click.command(help="List and modify expenses.")
@click.pass_obj
def expense(account):

    if account.context is 'add':
        prompt.add_transaction(account, 'Expense')
        echo.newline()

    elif account.context is 'edit':
        prompt.edit_transaction(account, 'Expense')
        echo.newline()

    elif account.context is 'delete':
        prompt.delete_transaction(account, 'Expense')
        echo.newline()


cli.add_command(income)
cli.add_command(expense)


if __name__ == '__main__':
    cli()
