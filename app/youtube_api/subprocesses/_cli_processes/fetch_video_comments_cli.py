""" a CLI that fetches comments from a YouTube video using the youtube api """
import argparse
import json

from subprocess_passthrough.subprocess_api_key import APIKey
from subprocess_passthrough.subprocess_api_client import YoutubeDataV3API
from subprocess_helper_functions.subprocess_output import print


class VideoCommentsCLI:
    """ a CLI that fetches comments from a YouTube video using the youtube api """
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Fetch comments as json from a YouTube video.'
        )

        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        self.parser.add_argument('video_id', type=str, help='The ID of the video to fetch comments from.')
        self.parser.add_argument('--token', type=str, help='An optional token for pagination.')
        self.parser.add_argument('--max-results', type=self.validate_max_results, default=10,
            help='The maximum number of results to return (1-100). Default is 10.'
        )

    @staticmethod
    def validate_max_results(value):
        """ confirms that the --max-results argument is a number within the allowed range """
        ivalue = int(value)
        if ivalue < 1 or ivalue > 100:
            raise argparse.ArgumentTypeError('max_results must be between 1 and 100 (inclusive).')
        return ivalue

    def run(self):
        """ runs the CLI application """
        self.args = self.parser.parse_args()
        response = self.fetch_comments_response(
            self.args.max_results,
            self.args.video_id,
            self.args.token
        )

        print(json.dumps(response, indent=4))

    @staticmethod
    def fetch_comments_response(
            max_results: int,
            video_id: str,
            token: str | None = None) -> dict:
        """ fetches YouTube comments using the API """
        youtube = YoutubeDataV3API(APIKey.VALUE)

        return youtube.client.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            maxResults=max_results,
            pageToken=token,
            order='relevance'
        ).execute()


if __name__ == '__main__':
    cli = VideoCommentsCLI()
    cli.run()
