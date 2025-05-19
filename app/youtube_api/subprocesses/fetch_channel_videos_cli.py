""" a CLI that fetches videos of a playlist using the YouTube api and returns as JSON """
import argparse
import json

from subprocess_api_key import APIKey
from subprocess_api_client import YoutubeDataV3API
from subprocess_output import print


class PlaylistVideosCLI:
    """ a CLI that fetches videos of a playlist using the YouTube api and returns as JSON """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Fetch JSON from a specific YouTube playlist.'
        )

        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        self.parser.add_argument('playlist_id', type=str, help='The ID of the YouTube playlist.')
        self.parser.add_argument('--token', type=str, help='An optional token for pagination.')
        self.parser.add_argument('--max-results', type=self.validate_max_results, default=10,
                help='The maximum number of results to return (1-50). Default is 10.'
        )

    @staticmethod
    def validate_max_results(value):
        """ confirms that the --max-results argument is a number within the allowed range """
        ivalue = int(value)
        if ivalue < 1 or ivalue > 50:
            raise argparse.ArgumentTypeError('max_results must be between 1 and 50 (inclusive).')
        return ivalue

    def run(self):
        """ runs the CLI application """
        self.args = self.parser.parse_args()
        response = self.fetch_playlist_videos(
            self.args.playlist_id,
            self.args.max_results,
            self.args.token
        )

        print(json.dumps(response, indent=4))

    @staticmethod
    def fetch_playlist_videos(
            playlist_id: str,
            max_results: int,
            token: str | None = None) -> dict:
        """ fetches videos of a playlist using the YouTube api and returns as JSON """
        youtube = YoutubeDataV3API(APIKey.VALUE)

        return youtube.client.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=max_results,
            pageToken=token
        ).execute()


if __name__ == '__main__':
    cli = PlaylistVideosCLI()
    cli.run()
