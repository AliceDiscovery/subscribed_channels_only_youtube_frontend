""" defines a dataclass that store information about a YouTube channel """
from .youtube_id_base_class import YoutubeIdType


class ChannelType(YoutubeIdType):
    """ a dataclass that store information about a YouTube channel """
    def __init__(self,
                 channel_id: str,
                 title: str,
                 subscriber_count: str,
                 description: str,
                 banner_url: str,
                 profile_pic_url: str,
                 date_created: str
                 ):
        super().__init__(channel_id)
        self._title = title
        self._subscriber_count = subscriber_count
        self._description = description
        self._banner_url = banner_url
        self._profile_pic_url = profile_pic_url
        self._date_created = date_created

    @property
    def channel_id(self):
        return self.youtube_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def subscribers(self) -> str:
        return self._subscriber_count

    @property
    def description(self) -> str:
        return self._description

    @property
    def banner(self) -> str:
        return self._banner_url

    @property
    def profile_pic(self) -> str:
        return self._profile_pic_url

    @property
    def date_created(self) -> str:
        return self._date_created
