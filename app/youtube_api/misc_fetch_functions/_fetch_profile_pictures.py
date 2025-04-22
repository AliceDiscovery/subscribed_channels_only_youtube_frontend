""" implements a function that retrieves the urls for YouTube profile icons """
from collections import OrderedDict
from threading import Thread

from .._api_client import YoutubeDataV3API

# cache stores already fetched profile icon urls
cache = OrderedDict()
MAX_CACHE_SIZE = 5000


def fetch_profile_pictures(api: YoutubeDataV3API, *channel_ids: [str | None]) -> [str]:
    """ retrieves the urls for YouTube profile icons """
    results = {}
    uncached_ids = [channel_id for channel_id in channel_ids if channel_id not in cache]

    def fetch_batch_of_icons(batch_of_ids: [str]):
        """ fetches the channel icons for a multiple channel ids (no more than 50) """
        request = api.client.channels().list(
            part='snippet',
            id=','.join(batch_of_ids)
        )
        response = request.execute()

        if 'items' in response:
            for item in response.get('items', []):
                channel_id = item.get('id', '')
                icon_url = item.get('snippet', {}).get('thumbnails', {}).get('default', {}).get('url', '')
                results[channel_id] = icon_url

                # Cache profile picture URL
                cache[channel_id] = icon_url
                while len(cache) > MAX_CACHE_SIZE:
                    cache.popitem(last=False)  # removes oldest profile pic from cache

    def chunk_and_fetch() -> dict:
        """ retrieves channel icons in batches of 50 """
        threads = []

        for i in range(0, len(uncached_ids), 50):
            batch_of_ids = uncached_ids[i:i + 50]
            thread = Thread(target=fetch_batch_of_icons, args=(batch_of_ids,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    # Fetch uncached icons
    if uncached_ids:
        fetched_results = chunk_and_fetch()
        results.update(fetched_results)

    # Combine cached and fetched icons
    for channel_id in channel_ids:
        results[channel_id] = cache.get(channel_id, results.get(channel_id))

    return [results.get(channel_id, None) for channel_id in channel_ids]


def fetch_profile_picture(api: YoutubeDataV3API, channel_id: str) -> str:
    """ retrieves the URL for the profile icon of a given channel id """
    return fetch_profile_pictures(api, channel_id)[0]
