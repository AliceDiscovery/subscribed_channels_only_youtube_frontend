from .video_base_class import VideoType


class VideoInfoType(VideoType):
    def __init__(self,
                 video_id: str,
                 title: str,
                 description: str|None,
                 views: str,
                 duration: str,
                 thumbnail_url: str):
        super().__init__(video_id)
        self._title = title
        self._description = description
        self._views = views
        self._duration = duration
        self._thumbnail_url = thumbnail_url

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str|None:
        return self._description

    @property
    def views(self) -> str:
        return self._views

    @property
    def duration(self) -> str:
        return self._duration

    @property
    def thumbnail(self) -> str:
        return self._thumbnail_url
