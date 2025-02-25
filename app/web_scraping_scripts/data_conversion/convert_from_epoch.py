""" defines a function to convert an epoch to a humanreadable date """
from datetime import datetime


def epoch_to_date(epoch: int) -> str:
    """ converts an epoch to a humanreadable date """
    return datetime.fromtimestamp(epoch).strftime('%Y/%m/%d')
