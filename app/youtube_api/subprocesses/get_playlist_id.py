""" a CLI that fetches search results using the YouTube api """
import argparse
from subprocess_api_key import APIKey
from subprocess_api_client import YoutubeDataV3API


class SearchQueryCLI:
    """ a CLI that fetches search results using the YouTube api """
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Fetches the playlist id of a given YouTube channel.'
        )

        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        self.parser.add_argument('channel_id', type=str, help='The query to process.')

    def run(self):
        """ runs the CLI application """
        self.args = self.parser.parse_args()
        response = self.get_playlist_id(channel_id=self.args.channel_id)
        print(response)

    @staticmethod
    def get_playlist_id(channel_id: str):
        """ fetches the playlist id of a given channel """
        youtube = YoutubeDataV3API(APIKey.VALUE)

        response = youtube.client.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()
        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']


if __name__ == '__main__':
    cli = SearchQueryCLI()
    cli.run()
