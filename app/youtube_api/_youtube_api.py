from googleapiclient.discovery import build
from .api_key import APIKey

from app.web_scraping_scripts import get_profile_icon, get_several_profile_icons
from app.web_scraping_scripts.data_conversion import convert_date, human_readable_large_numbers, human_readable_times

from app.validators import validate_video_id, validate_channel_id, ValidationError
from app.datatypes import VideoType, ChannelType, VideoPreviewType, CommentType


class YouTubeAPI:
    def __init__(self):
        self._api = build("youtube", "v3", developerKey=APIKey.VALUE)

    def get_video_page(self, video_id: str) -> VideoType:
        video = self.get_video_page_data(video_id)
        video.comments += self.get_video_comments(video_id=video_id, channel_id=video.channel_id)
        return video

    def get_video_page_data(self, video_id: str) -> VideoType:
        if not validate_video_id(video_id):
            raise ValidationError("Invalid video ID")

        request = self._api.videos().list(
            part="snippet,statistics",
            id=video_id
        )
        response = request.execute()

        video_data = response.get('items', [{}])[0]

        snippet = video_data.get('snippet', {})
        statistics = video_data.get('statistics', {})

        return VideoType(
            video_id=video_id,
            channel_name=snippet.get('channelTitle', ''),
            channel_id=snippet.get('channelId', ''),
            title=snippet.get('title', ''),
            views=statistics.get('viewCount', ''),
            description=snippet.get('description', ''),
            channel_pic=get_profile_icon(snippet.get('channelId')),
            date_stamp=convert_date(snippet.get('publishedAt'))
        )

    def get_video_comments(self, video_id: str, channel_id: str = None) -> [CommentType]:
        """ gets the first page of YouTube comments on a video. By passing the channel_id it saves an api call """

        if not validate_video_id(video_id):
            raise ValidationError('Invalid video ID')

        # gets the uploader's channel ID if it wasn't passed as an argument
        # this is in order to implement the CommentType.author_is_uploader value
        if channel_id is None:
            video_response = self._api.videos().list(
                part='snippet',
                id=video_id
            ).execute()

            if not video_response.get('items'):
                raise Exception('Invalid video ID or video not found')

            channel_id = video_response.get('items', [{}])[0].get('snippet', {}).get('channelId', '')

        comment_response = self._api.commentThreads().list(
            part='snippet,replies',
            videoId=video_id,
            maxResults=100,  # restrict to only the first 100 comments
            order='relevance'  # sort comments by relevance
        ).execute()

        comments = {}

        for root_comment in comment_response.get('items', []):
            snippet = root_comment.get('snippet', {}).get('topLevelComment', {}).get('snippet', {})
            author_channel_id = snippet.get('authorChannelId', {}).get('value', '')

            comment = CommentType(
                comment_id=root_comment.get('id', ''),
                text=snippet.get('textDisplay', ''),
                like_count=human_readable_large_numbers(snippet.get('likeCount', 0)),
                has_several_likes=(snippet.get('likeCount', 0) != 1),
                author_id=author_channel_id,
                author=snippet.get('authorDisplayName', ''),
                author_thumbnail_url=snippet.get('authorProfileImageUrl', ''),
                author_is_uploader=(author_channel_id == channel_id),
                author_is_verified=False,  # not available yet
                is_favorited=False,  # not available yet
                is_pinned=False,  # not available yet
                time_str=snippet.get('publishedAt', ''),
                replies=[],
                reply_count=0,
            )

            comments[comment.comment_id] = comment

            # process replies of the comment
            if 'replies' in root_comment:
                for reply_comment in root_comment.get('replies', {}).get('comments', []):
                    reply_snippet = reply_comment.get('snippet', '')
                    reply_author_channel_id = reply_snippet.get('authorChannelId', {}).get('value', '')

                    reply = CommentType(
                        comment_id=reply_comment['id'],
                        text=reply_snippet.get('textDisplay', ''),
                        like_count=human_readable_large_numbers(reply_snippet.get('likeCount', 0)),
                        has_several_likes=(reply_snippet.get('likeCount', 0) != 1),
                        author_id=reply_author_channel_id,
                        author=reply_snippet.get('authorDisplayName', ''),
                        author_thumbnail_url=reply_snippet.get('authorProfileImageUrl', ''),
                        author_is_uploader=(reply_author_channel_id == channel_id),
                        author_is_verified=False,  # not available yet
                        is_favorited=False,  # not available yet
                        is_pinned=False,  # not available yet
                        time_str=reply_snippet.get('publishedAt', ''),
                        replies=[],  # no nested replies
                        reply_count=0,
                    )
                    comment.replies.append(reply)
                    comment.reply_count += 1

        return comments.values()

    def get_search_results(self, query: str, max_results=10) -> [VideoPreviewType]:
        """ searches YouTube and returns results as a list of video previews """

        search_request = self._api.search().list(
            part='snippet',
            q=query,
            maxResults=max_results,
            type='video'  # restrict results to videos for now
        )
        search_response = search_request.execute()

        video_ids = [
            video['id']['videoId']
            for video in search_response.get('items', [])
            if video.get('id', {}).get('videoId')
        ]
        if not video_ids:
            return []

        video_request = self._api.videos().list(
            part='snippet,contentDetails,statistics',
            id=','.join(video_ids)
        )
        video_response = video_request.execute()

        channel_icons = get_several_profile_icons(
            *[video['snippet']['channelId']
                for video in video_response.get('items', [])
                if video.get('snippet', {}).get('channelId')
            ]
        )

        video_previews = []
        for video in video_response.get('items', []):
            video_id = video.get('id')
            if video_id:
                video_snippet = video.get('snippet', {})
                video_content_details = video.get('contentDetails', {})
                video_statistics = video.get('statistics', {})

                video = VideoPreviewType(
                    video_id=video_id,
                    channel_id=video_snippet.get('channelId', ''),
                    channel_name=video_snippet.get('channelTitle', ''),
                    title=video_snippet.get('title', ''),
                    views=human_readable_large_numbers(int(video_statistics.get('viewCount', 0))),
                    thumbnail=video_snippet.get('thumbnails', {}).get('high', {}).get('url', ''),
                    description=video_snippet.get('description', ''),
                    duration=video_content_details.get('duration', ''),  # this is returned in a different format
                    channel_pic=channel_icons.get(video_snippet.get('channelId'), ''),
                    date_stamp=convert_date(video_snippet.get('publishedAt'))
                )
                video_previews.append(video)

        return video_previews

    def get_channel_page(self, channel_id: str) -> [ChannelType, [VideoPreviewType]]:
        channel_data = self.get_channel_data(channel_id)
        first_page_of_videos = self.get_page_of_videos_from_channel(
            playlist_id=channel_data.playlist_id
        )
        return [channel_data, first_page_of_videos]

    def get_channel_data(self, channel_id: str) -> ChannelType:
        if not validate_channel_id(channel_id):
            raise ValidationError('Invalid channel ID')

        channel_response = self._api.channels().list(
            part='snippet,statistics,contentDetails,brandingSettings',
            id=channel_id
        ).execute()

        if not channel_response.get('items', []):
            raise ValidationError('Channel not found')

        channel_data = channel_response.get('items', [])[0]
        channel_snippet = channel_data.get('snippet', {})
        channel_statistics = channel_data.get('statistics', {})
        channel_content_details = channel_data.get('contentDetails', {})
        channel_branding = channel_data.get('brandingSettings', {})
        channel_info = ChannelType(
            channel_id=channel_id,
            banner=channel_branding.get('image', {}).get('bannerExternalUrl', ''),
            profile_pic=channel_snippet.get('thumbnails', {}).get('default', {}).get('url', None),
            title=channel_snippet.get('title', ''),
            handle=channel_snippet.get('customUrl', ''),
            subscribers=channel_statistics.get('subscriberCount', 0),
            num_videos=channel_statistics.get('videoCount', 0),
            playlist_id=channel_content_details.get('relatedPlaylists', {}).get('uploads', []),
            description=channel_snippet.get('description', '')
        )
        return channel_info

    def get_page_of_videos_from_channel(self, playlist_id: str, next_page_token=None) -> [VideoPreviewType]:
        video_id_response = self._api.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        video_ids = [video_id
                     for video in video_id_response.get('items', {})
                     if (video_id := video.get('snippet', {}).get('resourceId').get('videoId', ''))
                     ]

        # if there are no videos uploaded to the channel
        if not video_ids:
            return []

        videos = []

        video_response = self._api.videos().list(
            part='snippet,contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()

        for video_data in video_response.get('items', []):
            video_snippet = video_data.get('snippet', {})
            video_statistic = video_data.get('statistics', {})
            video_content_details = video_data.get('contentDetails', {})
            videos.append(VideoPreviewType(
                video_id=video_data.get('id', ''),
                title=video_snippet.get('title', ''),
                thumbnail=video_snippet.get('thumbnails', {}).get('default', {}).get('url', ''),
                views=video_statistic.get('viewCount', 0),
                description=video_snippet.get('description', ''),
                duration=video_content_details.get('duration', ''),
                date_stamp=video_snippet.get('publishedAt', '')
            ))

        return videos
