""" a CLI that fetches info about a specific YouTube channel as JSON"""
import argparse
import json

from subprocess_passthrough.subprocess_api_key import APIKey
from subprocess_passthrough.subprocess_api_client import YoutubeDataV3API
from subprocess_helper_functions.subprocess_output import print


class ChannelInfoCLI:
    """ a CLI that fetches info about a specific YouTube channel as JSON"""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Fetch info about a specific YouTube channel as JSON.'
        )

        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        self.parser.add_argument('channel_id', type=str, help='The ID of the YouTube channel.')

    def run(self):
        """ runs the CLI application """
        self.args = self.parser.parse_args()
        response = self.fetch_channel_info(self.args.channel_id)

        print(json.dumps(response, indent=4))

    @staticmethod
    def fetch_channel_info(channel_id: str) -> dict:
        """ fetches info about a channel """
        youtube = YoutubeDataV3API(APIKey.VALUE)

        return youtube.client.channels().list(
            part='snippet,statistics,contentDetails,brandingSettings',
            id=channel_id
        ).execute()


if __name__ == '__main__':
    cli = ChannelInfoCLI()
    cli.run()
