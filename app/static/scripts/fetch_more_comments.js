function hideMoreCommentsButtonIfNeeded() {
    if (nextPageToken == null) {
        document.getElementById('fetchMoreCommentsButton').classList.add("no-show");
    } else {
        document.getElementById('fetchMoreCommentsButton').classList.remove("no-show");
    }
}

function createCommentElement(commentData) {
    // Create comment container
    const comment = document.createElement('div');
    comment.className = 'comment';
    comment.id = commentData.id;

    // Pinned comment display
    if (commentData.is_pinned) {
        const pin = document.createElement('span');
        pin.className = 'pinned-by-uploader';
        pin.innerText = '📌 Pinned by creator';
        comment.append(pin);
    }

    // Author's profile picture
    const pfp = document.createElement('img');
    pfp.src = commentData.author_thumbnail_url;
    comment.appendChild(pfp);

    // Author info
    const author = document.createElement('span');
    author.className = 'comment-author';
    // Check if uploader
    if (commentData.author_is_uploader) author.classList.add('by-uploader');
    // Check if verified
    if (commentData.author_is_verified) {
        const check = document.createElement('span');
        check.className = 'author-verified';
        check.innerText = '✓';
        author.appendChild(check);
    }
    // Author name
    const authorLink = document.createElement('a');
    authorLink.href = '/channel/' + commentData.author_id;
    authorLink.innerText = commentData.author;
    author.appendChild(authorLink);
    // Post time
    const time = document.createTextNode(' '+commentData.time_str);
    author.appendChild(time);
    comment.appendChild(author);

    // Comment body
    const body = document.createElement('p');
    body.innerHTML = commentData.text;
    comment.appendChild(body);

    // Comment info
    const info = document.createElement('div');
    info.className = 'comment-info';
    // Likes
    const likes = document.createElement('span');
    likes.innerText = `${commentData.like_count} like`;
    if (commentData.has_several_likes) likes.innerText += 's';
    info.appendChild(likes);
    // Liked by creator
    if (commentData.is_favorited) {
        const div = document.createElement('div');
        div.className = 'liked-by-uploader';
        const span = document.createElement('span');
        span.innerText = '❤️ Liked by creator';
        div.appendChild(span);
        info.appendChild(div);
    }
    // Reply count
    if (commentData.reply_count > 0) {
        const div = document.createElement('div');
        const a = document.createElement('a');
        a.className = 'toggle-replies';
        a.setAttribute('data-reply-count', commentData.reply_count);
        div.appendChild(a);
        info.appendChild(div);
    }
    comment.appendChild(info);

    return comment;
}

function createReplyElement(replyData) {
    // Create reply container
    const reply = document.createElement('div');
    reply.className = 'reply';
    reply.id = replyData.id;

    // Pinned reply display
    if (replyData.is_pinned) {
        const pin = document.createElement('span');
        pin.className = 'pinned-by-uploader';
        pin.innerText = '📌 Pinned by creator';
        reply.append(pin);
    }

    // Author's profile picture
    const pfp = document.createElement('img');
    pfp.src = replyData.author_thumbnail_url;
    reply.appendChild(pfp);

    // Author info
    const author = document.createElement('span');
    author.className = 'comment-author';
    // Check if uploader
    if (replyData.author_is_uploader) author.classList.add('by-uploader');
    // Check if verified
    if (replyData.author_is_verified) {
        const check = document.createElement('span');
        check.className = 'author-verified';
        check.innerText = '✓';
        author.appendChild(check);
    }
    // Author name
    const authorLink = document.createElement('a');
    authorLink.href = '/channel/' + replyData.author_id;
    authorLink.innerText = replyData.author;
    author.appendChild(authorLink);
    // Post time
    const time = document.createTextNode(' '+replyData.time_str);
    author.appendChild(time);
    reply.appendChild(author);

    // reply body
    const body = document.createElement('p');
    body.innerHTML = replyData.text;
    reply.appendChild(body);

    // Reply info
    const info = document.createElement('div');
    info.className = 'comment-info';
    // Likes
    const likes = document.createElement('span');
    likes.innerText = `${replyData.like_count} like`;
    if (replyData.has_several_likes) likes.innerText += 's';
    info.appendChild(likes);
    // Liked by creator
    if (replyData.is_favorited) {
        const div = document.createElement('div');
        div.className = 'liked-by-uploader';
        const span = document.createElement('span');
        span.innerText = '❤️ Liked by creator';
        div.appendChild(span);
        info.appendChild(div);
    }
    reply.appendChild(info);

    return reply;
}

function createCommentBoxElement(commentData) {
    // Create container element
    const commentBox = document.createElement('div');
    commentBox.className = 'comment-box';

    // Create comment element
    const comment = createCommentElement(commentData);
    commentBox.appendChild(comment);

    // Create reply elements
    const replies = document.createElement('div');
    replies.className = 'replies hidden';
    for (const replyData of commentData.replies) {
        const reply = createReplyElement(replyData);
        replies.appendChild(reply);
    }
    commentBox.appendChild(replies);

    return commentBox;
}


function createPageElement(pageData) {
    const page = document.createElement("div");
    page.className = "page";

    pageData.forEach(commentData => {
        const videoElement = createCommentBoxElement(commentData);
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

