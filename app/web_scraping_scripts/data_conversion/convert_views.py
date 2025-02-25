""" Converts an integer into a humanreadable string """


def human_readable_views(num: int) -> str:
    """ Converts an integer into a humanreadable string """
    suffixes = ['', 'K', 'M', 'B']

    i = 0
    while num >= 1000 and i < len(suffixes) - 1:
        num /= 1000
        i += 1

    return f'{num:.1f}{suffixes[i]}'
