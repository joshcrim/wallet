import maya


def date(date):
    date = maya.when(str(date), timezone='US/Eastern')
    date = date.datetime().date()

    return date
