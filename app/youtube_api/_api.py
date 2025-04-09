from googleapiclient.discovery import build
from .api_key import APIKey


class API:
    CLIENT = build('youtube', 'v3', developerKey=APIKey.VALUE)
