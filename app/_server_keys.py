""" loads the server keys from the .env file """
import os
from dotenv import load_dotenv


def generate_key() -> str:
    """ randomly generates a new key """
    from secrets import token_hex
    return token_hex(32)


load_dotenv()


class ServerKey:
    """ A class that contains the server key """
    _VALUE = os.getenv("SECRET_KEY", generate_key())

    @classmethod
    @property
    def value(cls) -> str:
        return cls._VALUE
