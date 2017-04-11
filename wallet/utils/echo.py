import click
import crayons


def newline():
    return click.echo('\n', nl=False)


def blue(string, *args):
    return click.echo(
        crayons.blue(string.format(*args))
    )


def cyan(string, *args):
    return click.echo(
        crayons.cyan(string.format(*args))
    )


def red(string, *args):
    return click.echo(
        crayons.red(string.format(*args))
    )


def yellow(string, *args):
    return click.echo(
        crayons.yellow(string.format(*args))
    )


def transactions(transactions):
    for trans in transactions:
        if hasattr(trans, 'date'):
            blue('\t{0}', trans.date.strftime("%B %d, %Y"))

        if len(trans.name) <= 6:
            yellow("\t{0}:\t\t${1}", trans.name, trans.amount)

        else:
            yellow("\t{0}:\t${1}", trans.name, trans.amount)
