""" defines a function to convert a YouTube internal datestamp to a humanreadable date """


def convert_date(youtube_date_stamp: str | None) -> str | None:
    """ converts a YouTube internal datestamp to a humanreadable date """

    # Account for epoch being None
    if youtube_date_stamp is None:
        return None

    MONTH_MAP = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December'
    ]

    # maps number suffixes like "th" or "rd" using unicode
    SUFFIX_MAP = {
        '1': '\u02E2\u1D57',
        '2': '\u207F\u1D48',
        '3': '\u02B3\u1D48',
        '4': '\u1D57\u02B0',
        '5': '\u1D57\u02B0',
        '6': '\u1D57\u02B0',
        '7': '\u1D57\u02B0',
        '8': '\u1D57\u02B0',
        '9': '\u1D57\u02B0',
        '0': '\u1D57\u02B0'
    }

    youtube_date_stamp = youtube_date_stamp.replace('-', '')  # remove dashes from the date stamp

    year = youtube_date_stamp[:4]
    month_number = int(youtube_date_stamp[4:6]) - 1
    day = int(youtube_date_stamp[6:8]) - 1

    suffix = SUFFIX_MAP[str(day)[-1]]
    month = MONTH_MAP[month_number-1]
    return f"{day}{suffix} of {month} {year}"
