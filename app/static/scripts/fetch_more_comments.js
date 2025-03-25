function hideMoreCommentsButtonIfNeeded() {
    if (nextPageToken == null) {
        document.getElementById('fetchMoreCommentsButton').classList.add("no-show");
    } else {
        document.getElementById('fetchMoreCommentsButton').classList.remove("no-show");
    }
}

function createCommentElement(commentData) {
    const commentText = document.createElement('p');
    commentText.textContent = commentData.text;
    return commentText;
}


function createPageElement(pageData) {
    const page = document.createElement("div");
    page.className = "page";

    pageData.forEach(commentData => {
        const videoElement = createCommentElement(commentData);
        page.appendChild(videoElement);
    });

    const parentElement = document.getElementById('comments-section');
    parentElement.appendChild(page);
}


function fetchNextCommentPage(videoId, channelId, nextPageToken) {
    return fetch('/data/get-comments', {
        method: 'GET',
        headers: {
	    'video-id': videoId,
	    'channel-id': channelId,
            'next-page-token': nextPageToken
        }
    })
    .then(response => response.json());
}


function fetchMoreComments() {
    if (nextPageToken != null) {
        fetchNextCommentPage(videoId, channelId, nextPageToken)
            .then(data => {
                createPageElement(data.page);

                nextPageToken = data['next-page-token'];
		hideMoreCommentsButtonIfNeeded();
            });
    }
}


hideMoreCommentsButtonIfNeeded();
document.getElementById('fetchMoreCommentsButton').addEventListener('click', fetchMoreComments);

