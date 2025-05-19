""" a CLI that fetches search results using the youtube api """
import argparse
import json

from subprocess_api_key import APIKey
from subprocess_api_client import YoutubeDataV3API
from subprocess_output import print


class SearchQueryCLI:
    """ a CLI that fetches search results using the youtube api """
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Process a query, an optional token, and max results.'
        )

        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        self.parser.add_argument('query', type=str, help='The query to process.')
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
        response = self.fetch_search_response(
            self.args.max_results,
            self.args.query,
            self.args.token
        )

        print(json.dumps(response, indent=4))

    @staticmethod
    def fetch_search_response(
            max_results: int,
            search_query: str,
            token: str | None = None) -> dict:
        """ fetches YouTube search results using the API """
        youtube = YoutubeDataV3API(APIKey.VALUE)

        return youtube.client.search().list(
            part='snippet',
            q=search_query,
            maxResults=max_results,
            pageToken=token,
            type='video'  # restrict results to videos only
        ).execute()


if __name__ == '__main__':
    cli = SearchQueryCLI()
    cli.run()
