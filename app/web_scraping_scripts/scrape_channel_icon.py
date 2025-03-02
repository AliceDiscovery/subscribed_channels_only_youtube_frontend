""" implements a function that returns the url of a given channel's profile icon """
import requests
from bs4 import BeautifulSoup
from app.validators import validate_channel_id, ValidationError


def get_profile_icon(channel_id: str) -> str | None:
    """ a function that returns the url of a given channel's profile icon """
    if not validate_channel_id(channel_id):
        raise ValidationError

    url = f"https://www.youtube.com/channel/{channel_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    print('icon for', channel_id)

    if image_element := soup.find('link', {'rel': 'image_src'}):
        return image_element['href']
    return None
