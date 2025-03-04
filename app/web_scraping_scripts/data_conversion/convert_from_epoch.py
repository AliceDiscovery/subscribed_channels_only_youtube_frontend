""" defines a function to convert an epoch to a humanreadable date """
from datetime import datetime


def epoch_to_date(epoch: int | None) -> str | None:
    """ converts an epoch to a humanreadable date """

    # Account for epoch being None
    if epoch is None:
        return None

    return datetime.fromtimestamp(epoch).strftime('%Y/%m/%d')
