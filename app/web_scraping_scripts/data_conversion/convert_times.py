""" Converts a number of seconds into a humanreadable format """


def human_readable_times(seconds: int) -> str | None:
    """ Converts a number of seconds into a humanreadable format """

    # Account for seconds being None
    if seconds is None:
        return None

    seconds = int(seconds)  # convert possible float to int

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    sec = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02}:{sec:02}"
    else:
        return f"{minutes}:{sec:02}"

