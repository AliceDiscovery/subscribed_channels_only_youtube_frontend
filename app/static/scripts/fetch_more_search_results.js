let pageToken;


function hideNextPageButtonIfNeeded() {
    if (pageToken.is_last_page) {
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
    thumbnailContainer.href = videoData.video_url;

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
    titleLink.href = videoData.video_url;

    const titleContents = document.createElement('h2');
    titleContents.textContent = videoData.title;
    titleLink.appendChild(titleContents);

    videoContainer.appendChild(titleLink);

    // add channel info
    if (videoData.has_uploader_info) {
        console.log(videoData.uploader_info);
        const channelLink = document.createElement('a');
        channelLink.href = videoData.uploader_info.uploader_url;

        const channelContainer = document.createElement('div');
        channelContainer.className = 'channel-info';

        const channelImg = document.createElement('img');
        channelImg.src = videoData.uploader_info.profile_picture_url;
        channelImg.loading = 'lazy';
        channelContainer.appendChild(channelImg);

        const channelName = document.createElement('span');
        channelName.textContent = videoData.uploader_info.uploader;
        channelContainer.appendChild(channelName);

        channelLink.appendChild(channelContainer);

        videoContainer.appendChild(channelLink);
    }


    // add view count
    const viewCount = document.createElement('p');
    viewCount.textContent = `${videoData.view_count} views`;
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


function processPage(page) {
    createPageElement(page.page);
    pageToken = page.page_token;
}


function fetchMoreSearchResults() {
    if (!pageToken.is_last_page) {
        return fetch('/data/get-search-results', {
            method: 'GET',
            headers: {'token': JSON.stringify(pageToken)}
        })
    .then(response => response.json()).then(response => {
        processPage(response.data);
        hideNextPageButtonIfNeeded();
        });
    }
}


processPage(JSON.parse(data));
hideNextPageButtonIfNeeded();

document.getElementById('fetchMoreSearchResultsButton').addEventListener('click', fetchMoreSearchResults);