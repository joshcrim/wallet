import click
import crayons

import sys

from utils import (
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

        click.echo(
            crayons.yellow("New savings balance: {0}".format(account.wallet.savings))
        )

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
        click.echo('\n', nl=False)

        click.echo(
            crayons.cyan(
                "Wallet for {0} on {1}".format(
                    account.wallet, account.date.strftime("%B %d, %Y")
                )
            )
        )

        click.echo(
            crayons.yellow(
                "Savings balance: \t${0}".format(
                    account.wallet.calculate_savings_balance(account.date)
                )
            )
        )

        click.echo(
            crayons.yellow(
                "PayPeriod Savings: \t${0}".format(
                    account.payperiod.get_savings()
                )
            )
        )
        click.echo('\n', nl=False)

        click.echo(crayons.cyan("Income: ${0}".format(account.income_total)))
        format_transaction_output(account.incomes)
        click.echo('\n', nl=False)

        click.echo(crayons.cyan("Expenses: ${0}".format(account.expense_total)))
        format_transaction_output(account.expenses)
        click.echo('\n', nl=False)

        click.echo(crayons.cyan("Upcoming Expenses: ${0}".format(account.upcoming_total)))
        format_transaction_output(account.upcoming)
        click.echo('\n', nl=False)


@click.command(help="List and modify incomes.")
@click.pass_obj
def income(account):

    if account.context is 'add':
        prompt_add_transaction(account, 'Income')
        click.echo('\n', nl=False)

    elif account.context is 'edit':
        click.echo('Income Edit Success')
        prompt_edit_transaction(account, 'Income')
        click.echo('\n', nl=False)

    elif account.context is 'delete':
        click.echo('\n', nl=False)
        prompt_delete_transaction(account, 'Income')
        click.echo('\n', nl=False)


@click.command(help="List and modify expenses.")
@click.pass_obj
def expense(account):

    if account.context is 'add':
        click.echo('\n', nl=False)
        prompt_add_transaction(account, 'Expense')
        click.echo('\n', nl=False)

    elif account.context is 'edit':
        click.echo('\n', nl=False)
        prompt_edit_transaction(account, 'Expense')
        click.echo('\n', nl=False)

    elif account.context is 'delete':
        click.echo('\n', nl=False)
        prompt_delete_transaction(account, 'Expense')
        click.echo('\n', nl=False)


cli.add_command(income)
cli.add_command(expense)


if __name__ == '__main__':
    cli()
