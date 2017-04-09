import click

import sys

from . import cli_utils as cu
from .utils import (
    format_transaction_output,
    parse_date,
    prompt_add_transaction,
    prompt_delete_transaction,
    prompt_edit_transaction
)

from accounts.models import Wallet


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
            cu.output_red("Select a date of today or later.")
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
@click.option('--add', type=click.Choice(['income', 'expense']))
@click.option('--edit', type=click.Choice(['income', 'expense']))
@click.option('--delete', type=click.Choice(['income', 'expense']))
@click.pass_context
def cli(ctx, date=None, setsavings=None, add=None, edit=None, delete=None, help=False):

    account = ctx.obj = Account(date=date)

    options = {
        'income': income,
        'expense': expense,
    }

    if setsavings:
        account.wallet.update_savings(setsavings)

        cu.output_yellow("New savings balance: {0}", account.wallet.savings)

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
        cu.newline()

        cu.output_cyan(
            "Wallet for {0} on {1}",
            account.wallet,
            account.date.strftime("%B %d, %Y")
        )

        cu.output_yellow(
            "Savings balance: \t${0}",
            account.wallet.calculate_savings_balance(account.date)
        )

        cu.output_yellow(
            "PayPeriod Savings: \t${0}",
            account.payperiod.get_savings()
        )

        cu.newline()

        cu.output_cyan("Income: ${0}", account.income_total)
        format_transaction_output(account.incomes)

        cu.newline()

        cu.output_cyan("Expenses: ${0}", account.expense_total)
        format_transaction_output(account.expenses)

        cu.newline()

        cu.output_cyan("Upcoming Expenses: ${0}", account.upcoming_total)
        format_transaction_output(account.upcoming)

        cu.newline()


@click.command(help="List and modify incomes.")
@click.pass_obj
def income(account):

    if account.context is 'add':
        prompt_add_transaction(account, 'Income')
        cu.newline()

    elif account.context is 'edit':
        prompt_edit_transaction(account, 'Income')
        cu.newline()

    elif account.context is 'delete':
        prompt_delete_transaction(account, 'Income')
        cu.newline()


@click.command(help="List and modify expenses.")
@click.pass_obj
def expense(account):

    if account.context is 'add':
        prompt_add_transaction(account, 'Expense')
        cu.newline()

    elif account.context is 'edit':
        prompt_edit_transaction(account, 'Expense')
        cu.newline()

    elif account.context is 'delete':
        prompt_delete_transaction(account, 'Expense')
        cu.newline()


cli.add_command(income)
cli.add_command(expense)


if __name__ == '__main__':
    cli()
