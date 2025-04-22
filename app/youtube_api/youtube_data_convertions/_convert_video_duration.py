""" converts an ISO 8601 duration into a formated duration string """
from isodate import parse_duration
from datetime import timedelta


def convert_iso_duration(iso_duration: str) -> str:
    """ converts a ISO 8601 duration into a formated duration string """

    # live streems
    if iso_duration == 'P0D':
        return 'LIVE'

    total_seconds = int(parse_duration(iso_duration).total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours > 0:
        return f'{hours}:{minutes:02}:{seconds:02}'
    return f'{minutes:02}:{seconds:02}'
