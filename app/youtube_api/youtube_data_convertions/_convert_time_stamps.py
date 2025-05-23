""" converts iso date stamp to human readable delta """
from datetime import datetime, timezone


def human_readable_time_delta(timestamp):
    """ converts iso date stamp to human readable delta """
    delta = datetime.now(timezone.utc) - datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    total_seconds = int(delta.total_seconds())

    just_now_threshold_seconds = 300  # Threshold for "Just now" (in seconds)

    if total_seconds < just_now_threshold_seconds:
        return 'Just now'

    units = [
        ('year', 31536000),  # assumes 365 days in a year
        ('month', 2592000),  # assumes 30 days in a month
        ('week', 604800),
        ('day', 86400),
        ('hour', 3600),
        ('minute', 60),
        ('second', 1)
    ]

    for unit, seconds_in_unit in units:
        if total_seconds >= seconds_in_unit:
            value = total_seconds // seconds_in_unit
            return f"{value} {unit}{'s' if value != 1 else ''} ago"
    return 'Just now'  # fallback
