""" converts an ISO 8601 duration into a formated duration string """
from isodate import parse_duration, isoerror


def convert_iso_duration(iso_duration: str) -> str:
    """ converts a ISO 8601 duration into a formated duration string """

    # live streams
    if iso_duration == 'P0D':
        return 'LIVE'

    try:
        total_seconds = int(parse_duration(iso_duration).total_seconds())
    except isoerror.ISO8601Error:
        return 'Error'
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f'{hours}:{minutes:02}:{seconds:02}'
    return f'{minutes:02}:{seconds:02}'
