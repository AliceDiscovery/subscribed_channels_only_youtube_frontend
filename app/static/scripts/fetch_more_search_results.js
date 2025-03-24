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
    viewCount.textContent = videoData.views;

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
		console.log(data);
                createPageElement(data.page);

                nextPageToken = data['next-page-token'];
		hideNextPageButtonIfNeeded();
            });
    }
}


hideNextPageButtonIfNeeded();
document.getElementById('fetchMoreSearchResultsButton').addEventListener('click', fetchMoreSearchResults);

