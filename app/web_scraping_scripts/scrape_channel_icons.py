""" implements a function that returns the url of a given channel's profile icon """
import requests
from bs4 import BeautifulSoup

from threading import Thread
from queue import Queue

from app.validators import validate_channel_id, ValidationError


def get_profile_icon(channel_id: str) -> str | None:
    """ a function that returns the url of a given channel's profile icon """
    if not validate_channel_id(channel_id):
        raise ValidationError

    url = f"https://www.youtube.com/channel/{channel_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    if image_element := soup.find('link', {'rel': 'image_src'}):
        return image_element['href']
    return None


def get_several_profile_icons(*channel_ids: str) -> dict:
    """ returns the urls of profile icons for several channels in parallel """
    queue = Queue()
    threads = []
    profile_icon_dict = {}

    def thread_wrapper(channel_id):
        profile_icon = get_profile_icon(channel_id)
        queue.put((channel_id, profile_icon))

    for channel_id in channel_ids:
        thread = Thread(target=thread_wrapper, args=(channel_id,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    while not queue.empty():
        channel_id, profile_icon = queue.get()
        profile_icon_dict[channel_id] = profile_icon

    return profile_icon_dict
