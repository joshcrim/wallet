import click
import crayons


def newline():
    return click.echo('\n', nl=False)


def output_blue(string, *args):
    return click.echo(
        crayons.blue(string.format(*args))
    )


def output_cyan(string, *args):
    return click.echo(
        crayons.cyan(string.format(*args))
    )


def output_red(string, *args):
    return click.echo(
        crayons.red(string.format(*args))
    )


def output_yellow(string, *args):
    return click.echo(
        crayons.yellow(string.format(*args))
    )
