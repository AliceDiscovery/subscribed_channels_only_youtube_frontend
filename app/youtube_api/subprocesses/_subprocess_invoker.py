from pathlib import Path
from subprocess import check_output, CalledProcessError
from sys import executable as python_path


_subprocess_dir = Path(__file__).parent / '_cli_processes'


class Subprocess:
    """ represents a single CLI subprocess that can be invoked."""
    def __init__(self, script_name: str):
        self.script_path = _subprocess_dir / script_name
        if not self.script_path.exists():
            raise FileNotFoundError(f'The script "{script_name}" does not exist in the subprocesses directory.')

    def invoke(self, *args) -> str | None:
        """invokes a subprocess and returns its output."""
        try:
            return check_output([python_path, str(self.script_path)] + list(args)).decode('utf-8')
        except CalledProcessError:
            return None


FETCH_CHANNEL_VIDEOS = Subprocess('fetch_channel_videos_cli.py')
FETCH_PROFILE_PICTURE = Subprocess('fetch_profile_pictures_cli.py')
FETCH_SEARCH_RESULTS = Subprocess('fetch_search_results_cli.py')
FETCH_VIDEO_COMMENTS = Subprocess('fetch_video_comments_cli.py')
FETCH_VIDEO_PREVIEWS = Subprocess('fetch_video_preview_data.py')
FETCH_CHANNEL_PLAYLIST_ID = Subprocess('get_playlist_id.py')
FETCH_UPLOADER_ID = Subprocess('get_uploader_id.py')

__all__ = [
    "FETCH_CHANNEL_VIDEOS",
    "FETCH_PROFILE_PICTURE",
    "FETCH_SEARCH_RESULTS",
    "FETCH_VIDEO_COMMENTS",
    "FETCH_VIDEO_PREVIEWS",
    "FETCH_CHANNEL_PLAYLIST_ID",
    "FETCH_UPLOADER_ID"
]
