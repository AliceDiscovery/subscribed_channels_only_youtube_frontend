""" a safe version of `print` that suppresses BrokenPipeError """


built_in_print = print


def print(*args, **kwargs) -> None:
    """ a safe version of `print` that suppresses BrokenPipeError """
    kwargs.setdefault('end', '')
    try:
        built_in_print(*args, **kwargs)
    except BrokenPipeError:
        pass
