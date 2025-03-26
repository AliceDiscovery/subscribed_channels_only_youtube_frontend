function hideNextPageButtonIfNeeded() {
    if (nextPageToken == null) {
	document.getElementById('fetchMoreSearchResultsButton').classList.add("no-show");
    } else {
	document.getElementById('fetchMoreSearchResultsButton').classList.remove("no-show");
    }
}


function createVideoElement(videoData) {
    const videoContainer = document.createElement('div');
    videoContainer.className = 'video-container';


    // add thumbnail
    const thumbnailContainer = document.createElement('a');
    thumbnailContainer.className = 'thumbnail-container';
    thumbnailContainer.href = `/video/${videoData.video_id}`;

    const thumbnailImg = document.createElement('img');
    thumbnailImg.src = videoData.thumbnail;
    thumbnailImg.loading = 'lazy';
    thumbnailContainer.appendChild(thumbnailImg);

    const durationOverlay = document.createElement('span');
    durationOverlay.textContent = videoData.duration;
    thumbnailContainer.appendChild(durationOverlay);

    videoContainer.appendChild(thumbnailContainer);


    // add title
    const titleLink = document.createElement('a');
    titleLink.href = `/video/${videoData.video_id}`;

    const titleContents = document.createElement('h2');
    titleContents.textContent = videoData.title;
    titleLink.appendChild(titleContents);

    videoContainer.appendChild(titleLink);

    // add channel info
    const channelLink = document.createElement('a');
    channelLink.href = `/channel/${videoData.channel_id}`;

    const channelContainer = document.createElement('div');
    channelContainer.className = 'channel-info';
    
    const channelImg = document.createElement('img');
    channelImg.src = videoData.channel_pic;
    channelImg.loading = 'lazy';
    channelContainer.appendChild(channelImg);

    const channelName = document.createElement('span');
    channelName.textContent = videoData.channel_name;
    channelContainer.appendChild(channelName);

    channelLink.appendChild(channelContainer);

    videoContainer.appendChild(channelLink);


    // add view count
    const viewCount = document.createElement('p');
    viewCount.textContent = `${videoData.views} views`;
    videoContainer.appendChild(viewCount);

    // add description
    const description = document.createElement('p');
    description.textContent = videoData.description;
    videoContainer.appendChild(description);


    return videoContainer;
}

function createPageElement(pageData) {
    const page = document.createElement("div");
    page.className = "page";

    pageData.forEach(videoData => {
        const videoElement = createVideoElement(videoData);
        page.appendChild(videoElement);
    });

    const parentElement = document.getElementById('videos');
    parentElement.appendChild(page);
}




function fetchNextSearchResultsPage(query, nextPageToken) {
    return fetch('/data/get-search-results', {
        method: 'GET',
        headers: {
            'query': query,
            'next-page-token': nextPageToken
        }
    })
    .then(response => response.json());
}




function fetchMoreSearchResults() {
    if (nextPageToken != null) {
        fetchNextSearchResultsPage(query, nextPageToken)
            .then(data => {
                createPageElement(data.page);

                nextPageToken = data['next-page-token'];
		hideNextPageButtonIfNeeded();
            });
    }
}


hideNextPageButtonIfNeeded();
document.getElementById('fetchMoreSearchResultsButton').addEventListener('click', fetchMoreSearchResults);

