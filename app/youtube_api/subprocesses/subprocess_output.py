""" a safe version of `print` that suppresses BrokenPipeError """


built_in_print = print


def print(*args, **kvargs) -> None:
    """ a safe version of `print` that suppresses BrokenPipeError """
    try:
        built_in_print(*args, **kvargs)
    except BrokenPipeError:
        pass
