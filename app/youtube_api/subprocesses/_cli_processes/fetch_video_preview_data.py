import argparse
import json

from subprocess_passthrough.subprocess_api_key import APIKey
from subprocess_passthrough.subprocess_api_client import YoutubeDataV3API
from subprocess_helper_functions.subprocess_output import print


class VideoDataCLI:
    """ A CLI that fetches data required for building previews from multiple YouTube videos using the YouTube API """

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Fetch video preview data as JSON from YouTube videos.'
        )

        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        self.parser.add_argument('video_ids', type=str, nargs='+',
                                 help='The IDs of the videos to fetch data from (space-separated).')

    def run(self):
        """ Runs the CLI application """
        self.args = self.parser.parse_args()

        if len(self.args.video_ids) > 50:
            raise argparse.ArgumentTypeError('No more than 50 video IDs can be provided.')

        response = self.fetch_video_data_response(
            self.args.video_ids
        )

        print(json.dumps(response, indent=4))

    @staticmethod
    def fetch_video_data_response(video_ids: list) -> dict:
        """ Fetches YouTube video data using the API """
        youtube = YoutubeDataV3API(APIKey.VALUE)

        video_response = youtube.client.videos().list(
            part='snippet,contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()

        return video_response


if __name__ == '__main__':
    cli = VideoDataCLI()
    cli.run()
