""" a CLI that fetches the channel id of a video's uploader """
import argparse

from subprocess_passthrough.subprocess_api_key import APIKey
from subprocess_passthrough.subprocess_api_client import YoutubeDataV3API
from subprocess_helper_functions.subprocess_output import print


class GetUploaderId:
    """ a CLI that fetches the channel id of a video's uploader """
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description='Fetches the channel id of a video\'s uploader'
        )

        self._setup_arguments()
        self.args = None

    def _setup_arguments(self):
        self.parser.add_argument('video_id', type=str, help='The target video\'s id')

    def run(self):
        """ runs the CLI application """
        self.args = self.parser.parse_args()
        response = self.get_uploader_id(video_id=self.args.video_id)
        print(response)

    @staticmethod
    def get_uploader_id(video_id: str) -> str:
        """ Fetches the video's uploader's id. """
        youtube = YoutubeDataV3API(APIKey.VALUE)

        video_response = youtube.client.videos().list(
            part='snippet',
            id=video_id
        ).execute()

        if not video_response.get('items'):
            raise ValueError('Invalid video ID or video not found')

        try:
            return video_response.get('items', [{}])[0].get('snippet', {})['channelId']
        except KeyError as error:
            new_error_msg = f'{error}\nYouTube has changed their json when extracting the uploader\'s id;'
            raise KeyError(new_error_msg) from error


if __name__ == '__main__':
    cli = GetUploaderId()
    cli.run()
