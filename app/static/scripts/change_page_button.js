let next_page_token = null;


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

function createPageElement(pageData) {
    // add logic to create a new page
    console.log(pageData);
}


document.getElementById('nextPageButton').addEventListener('click', function() {
    fetchNextChannelPage(playlist_id, next_page_token)
        .then(data => {
            next_page_token = data['next-page-token'];
	    createPageElement(data.page);
        });
});

