""" A CLI that fetches the profile pictures channels using the YouTube API """
from threading import Thread

import argparse
import json

from subprocess_passthrough.subprocess_api_key import APIKey
from subprocess_passthrough.subprocess_api_client import YoutubeDataV3API
from subprocess_helper_functions.subprocess_output import print


class FetchProfilePicturesCLI:
    """ A CLI that fetches the profile pictures channels using the YouTube API """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Fetches the URLs for given channels\' the profile pictures.'
        )

        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        self.parser.add_argument('channel_ids', type=str, nargs='+',
                                 help='The IDs of the channels to fetch the profile pictures from (space-separated).')

    def run(self):
        """ Runs the CLI application """
        self.args = self.parser.parse_args()

        profile_picture_array = self.fetch_profile_pictures(*self.args.channel_ids)

        print(json.dumps(profile_picture_array, indent=4))

    @staticmethod
    def fetch_profile_pictures(*channel_ids: [str | None]) -> [str]:
        """ retrieves the urls for YouTube profile icons """
        youtube = YoutubeDataV3API(APIKey.VALUE)
        results = {}

        def fetch_batch_of_icons(batch_of_ids: [str]):
            """ fetches the channel icons for a multiple channel ids (no more than 50) """
            request = youtube.client.channels().list(
                part='snippet',
                id=','.join(batch_of_ids)
            )
            response = request.execute()

            if 'items' in response:
                try:
                    for item in response['items']:
                        try:
                            channel_id = item['id']
                            results[channel_id] = item['snippet']['thumbnails']['default']['url']
                        except KeyError as error:
                            new_error_msg = f'{error}\nYouTube has changed their json when fetching profile pictures.'
                            raise KeyError(new_error_msg) from error

                except KeyError as error:
                    new_error_msg = f'{error}\nYouTube has changed their json and removed the "items" array.'
                    raise KeyError(new_error_msg) from error

        def chunk_and_fetch(channel_ids: [str]) -> dict | str:
            """ retrieves channel icons in batches of 50 """
            unique_ids = list(set(channel_ids))

            threads = []

            for i in range(0, len(unique_ids), 50):
                batch_of_ids = unique_ids[i:i + 50]
                thread = Thread(target=fetch_batch_of_icons, args=(batch_of_ids,))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            return results

        return chunk_and_fetch(channel_ids)


if __name__ == '__main__':
    cli = FetchProfilePicturesCLI()
    cli.run()
