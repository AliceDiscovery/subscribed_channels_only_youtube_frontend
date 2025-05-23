""" loads the api key form the .env file """
import os
from dotenv import load_dotenv


load_dotenv()


class APIKey:
    """ A class that contains the API in a property called 'VALUE' """
    VALUE = os.getenv("API_KEY")
