function createVideoElement(videoData) {
    const videoContainer = document.createElement('div');
    videoContainer.className = 'video-container';

    // create thumbnail container and it's contents
    const thumbnailContainer = document.createElement('a');
    thumbnailContainer.className = 'thumbnail-container';
    thumbnailContainer.href = `/video/${videoData.video_id}`;

    const thumbnailImg = document.createElement('img');
    thumbnailImg.src = videoData.thumbnail;
    thumbnailImg.loading = 'lazy';

    const durationOverlay = document.createElement('span');
    durationOverlay.textContent = videoData.duration;

    thumbnailContainer.appendChild(thumbnailImg);
    thumbnailContainer.appendChild(durationOverlay);


    // video info
    const viewCount = document.createElement('p');
    viewCount.textContent = `${videoData.views} views`;

    const titleLink = document.createElement('a');
    titleLink.href = `/video/${videoData.video_id}`;

    const titleContents = document.createElement('h2');
    titleContents.textContent = videoData.title;
    titleLink.appendChild(titleContents);

    // append the contents to the video container element
    videoContainer.appendChild(thumbnailContainer);
    videoContainer.appendChild(viewCount);
    videoContainer.appendChild(titleLink);

    return videoContainer;
}

function createPageElement(pageData) {
    const page = document.createElement("div");
    page.className = "page";

    pageData.forEach(videoData => {
        const videoElement = createVideoElement(videoData);
        page.appendChild(videoElement);
    });

    const parentElement = document.getElementById('video-feed');
    parentElement.appendChild(page);
}




let nextPageToken = null;


function fetchNextChannelPage(playlistId, nextPageToken) {
    return fetch('/data/get-channel-videos', {
        method: 'GET',
        headers: {
            'playlist-id': playlistId,
            'next-page-token': nextPageToken
        }
    })
    .then(response => response.json());
}

document.getElementById('nextPageButton').addEventListener('click', function() {
    fetchNextChannelPage(playlist_id, nextPageToken)
        .then(data => {
            nextPageToken = data['next-page-token'];
	    createPageElement(data.page);
        });
});

