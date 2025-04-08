""" fetch profile icons from channel ids """
from threading import Thread


def fetch_profile_pictures(api, *channel_ids: [str]) -> [str]:
    """ retrieves the urls for YouTube profile icons """

    def fetch_batch_of_icons(batch_of_ids: [str], results):
        """ fetches the channel icons for a multiple channel ids (no more than 50) """
        request = api.channels().list(
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
        results = {}

        for i in range(0, len(channel_ids), 50):
            batch_of_ids = channel_ids[i:i + 50]
            thread = Thread(target=fetch_batch_of_icons, args=(batch_of_ids, results))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        return results

    profile_pics = chunk_and_fetch()
    return [profile_pics[channel_id] for channel_id in channel_ids]
