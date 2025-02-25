""" implements base class for a YouTube video """


class VideoType:
    """ base class to represent a YouTube video """
    def __init__(self, video_id: str):
        self._video_id = video_id

    @property
    def video_id(self):
        """ returns the video id """
        return self._video_id
