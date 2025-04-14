let pageToken;


function hideMoreCommentsButtonIfNeeded() {
    if (pageToken.is_last_page) {
        document.getElementById('fetchMoreCommentsButton').classList.add("no-show");
    } else {
        document.getElementById('fetchMoreCommentsButton').classList.remove("no-show");
    }
}


function createCommentElement(commentData) {
    // Create comment container
    const comment = document.createElement('div');
    comment.className = 'comment';
    comment.id = commentData.comment_id;

    // Author's profile picture
    const pfp = document.createElement('img');
    pfp.src = commentData.author_thumbnail_url;
    comment.appendChild(pfp);

    // Author info
    const author = document.createElement('span');
    author.className = 'comment-author';
    // Check if uploader
    if (commentData.is_author_uploader) author.classList.add('by-uploader');

    // Author name
    const authorLink = document.createElement('a');
    authorLink.href = commentData.author_url
    authorLink.innerText = commentData.author;
    author.appendChild(authorLink);

    // Post time
    const time = document.createTextNode(' '+commentData.time_stamp_formatted);
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
    likes.innerText = commentData.like_count_formatted;
    info.appendChild(likes);

    // Reply count
    if (commentData.has_replies) {
        const div = document.createElement('div');
        const a = document.createElement('a');
        a.className = 'toggle-replies';
        a.setAttribute('data-reply-count', commentData.reply_count_formatted);
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
    reply.id = replyData.comment_id;

    // Author's profile picture
    const pfp = document.createElement('img');
    pfp.src = replyData.author_thumbnail_url;
    reply.appendChild(pfp);

    // Author info
    const author = document.createElement('span');
    author.className = 'comment-author';

    // Check if uploader
    if (replyData.author_is_uploader) author.classList.add('by-uploader');

    // Author name
    const authorLink = document.createElement('a');
    authorLink.href = replyData.author_url;
    authorLink.innerText = replyData.author;
    author.appendChild(authorLink);

    // Post time
    const time = document.createTextNode(' '+replyData.time_stamp_formatted);
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
    likes.innerText = replyData.like_count_formatted;
    info.appendChild(likes);

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

    // Add show replies button functionality
    const replyButtons = commentBox.querySelectorAll('.toggle-replies');
    initializeCollapsableReplies(replyButtons)

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


function processPage(page) {
    createPageElement(page.page);
    pageToken = page.page_token;
}


function fetchMoreComments() {
    if (!pageToken.is_last_page) {
        return fetch('/data/get-comments', {
            method: 'GET',
            headers: {'token': JSON.stringify(pageToken)}
        })
    .then(response => response.json()).then(response => {
        processPage(response.data);
        hideMoreCommentsButtonIfNeeded();
        });
    }
}


processPage(JSON.parse(commentData));
hideMoreCommentsButtonIfNeeded();

document.getElementById('fetchMoreCommentsButton').addEventListener('click', fetchMoreComments);
