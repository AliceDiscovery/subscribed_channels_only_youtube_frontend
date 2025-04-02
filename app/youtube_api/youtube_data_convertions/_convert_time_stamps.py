""" converts iso date stamp to human readable delta """
from datetime import datetime, timezone


def human_readable_time_delta(timestamp):
    """ converts iso date stamp to human readable delta """
    delta = datetime.now(timezone.utc) - datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    total_seconds = int(delta.total_seconds())

    if total_seconds < 60:
        return f"{total_seconds} seconds ago"
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    elif total_seconds < 86400:
        hours = total_seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = total_seconds // 86400
        return f"{days} day{'s' if days != 1 else ''} ago"
