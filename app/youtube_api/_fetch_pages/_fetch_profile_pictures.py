""" fetch profile icons from channel ids """
from threading import Thread

from .._api import API


def fetch_profile_pictures(*channel_ids: [str|None]) -> [str]:
    """ retrieves the urls for YouTube profile icons """
    results = {}

    def fetch_batch_of_icons(batch_of_ids: [str]):
        """ fetches the channel icons for a multiple channel ids (no more than 50) """
        request = API.CLIENT.channels().list(
            part='snippet',
            id=','.join(batch_of_ids)
        )
        response = request.execute()

        if 'items' in response:
            for item in response.get('items', []):
                channel_id = item.get('id', '')
                results[channel_id] = item.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', '')

    def chunk_and_fetch() -> dict | str:
        """ retrieves channel icons in batches of 50 """
        threads = []

        for i in range(0, len(channel_ids), 50):
            batch_of_ids = channel_ids[i:i + 50]
            thread = Thread(target=fetch_batch_of_icons, args=(batch_of_ids, ))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    profile_pics = chunk_and_fetch()
    return [profile_pics.get(channel_id, None) for channel_id in channel_ids]
