""" a CLI that fetches the playlist id for a given channel """
import argparse

from subprocess_passthrough.subprocess_api_key import APIKey
from subprocess_passthrough.subprocess_api_client import YoutubeDataV3API
from subprocess_helper_functions.subprocess_output import print


class GetPlaylistIdCLI:
    """ a CLI that fetches the playlist id for a given channel """
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Fetches the playlist id of a given YouTube channel.'
        )

        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        self.parser.add_argument('channel_id', type=str, help='The target channel\'s ID')

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
    cli = GetPlaylistIdCLI()
    cli.run()
