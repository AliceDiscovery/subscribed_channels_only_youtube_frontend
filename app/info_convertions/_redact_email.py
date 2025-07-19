""" generates a censored form of an email address """


def redact_email(email: str) -> str:
    """ generates a censored form of an email address """
    try:
        local_part, domain = email.split('@')
    except ValueError as error:
        raise ValueError(f'"{email}" is missing an "@" symbol.') from error
    else:
        if not local_part or not domain:
            raise ValueError(f'"{email}" is invalid.')

    if len(local_part) > 2:
        redacted_local = local_part[0] + '*' * (len(local_part) - 2) + local_part[-1]
    else:
        redacted_local = '*' * len(local_part)

    # for short addresses, censor the last character of the local_part also.
    if len(redacted_local) < 6:
        redacted_local = redacted_local[:-1] + '*'

    return f'{redacted_local}@{domain}'
