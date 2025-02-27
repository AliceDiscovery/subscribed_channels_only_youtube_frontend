""" Converts large integers into humanreadable strings """


def human_readable_large_numbers(num: int) -> str:
    """ Converts a large integer into a humanreadable string """
    suffixes = ['', 'K', 'M', 'B']

    i = 0
    while num >= 1000 and i < len(suffixes) - 1:
        num /= 1000
        i += 1

    return f'{num:.1f}{suffixes[i]}'
