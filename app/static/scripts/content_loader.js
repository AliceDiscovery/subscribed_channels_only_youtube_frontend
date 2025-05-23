function createVideoElement(videoData) {
    function createThumbnailContainer() {
        const thumbnailContainer = document.createElement('a');
        thumbnailContainer.href = videoData.video_url;

        const thumbnailImg = document.createElement('img');
        thumbnailImg.src = videoData.thumbnail;
        thumbnailImg.loading = 'lazy';
        thumbnailContainer.appendChild(thumbnailImg);

        const durationOverlay = document.createElement('span');
        durationOverlay.textContent = videoData.duration;
        thumbnailContainer.appendChild(durationOverlay);

        return thumbnailContainer;
    }

    function createTitleContainer() {
        const titleLink = document.createElement('a');
        titleLink.href = videoData.video_url;

        const titleContents = document.createElement('h2');
        titleContents.textContent = videoData.title;
        titleLink.appendChild(titleContents);

        return titleLink;
    }

    function createChannelInfoContainer() {
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

        return channelLink;
    }

    function createViewCountElement() {
        const viewCount = document.createElement('p');
        viewCount.textContent = `${videoData.view_count} views`;
        return viewCount;
    }

    function createDescriptionElement() {
        const description = document.createElement('p');
        description.textContent = videoData.description;
        return description;
    }

    const videoContainer = document.createElement('div');
    videoContainer.className = 'video-container';

    videoContainer.appendChild(createThumbnailContainer());
    videoContainer.appendChild(createTitleContainer());
    if (videoData.has_uploader_info) {
        videoContainer.appendChild(createChannelInfoContainer());
    }
    videoContainer.appendChild(createViewCountElement());
    videoContainer.appendChild(createDescriptionElement());

    return videoContainer;
}


function createNewCommentsPage(commentData) {
    function createProfilePicture(data) {
        const pfp = document.createElement('img');
        pfp.src = data.author_thumbnail_url;
        return pfp;
    }

    function createAuthorInfo(data, isReply) {
        const author = document.createElement('span');
        author.className = 'comment-author';
        if (isReply ? data.author_is_uploader : data.is_author_uploader) {
            author.classList.add('by-uploader');
        }

        const authorLink = document.createElement('a');
        authorLink.href = data.author_url;
        authorLink.innerText = data.author;

        author.appendChild(authorLink);

        const time = document.createTextNode(' ' + data.time_stamp_formatted);
        author.appendChild(time);

        return author;
    }

    function createBody(data) {
        const body = document.createElement('p');
        body.innerHTML = data.text;
        return body;
    }

    function createInfo(data, isReply) {
        const info = document.createElement('div');
        info.className = 'comment-info';

        const likes = document.createElement('span');
        likes.innerText = data.like_count_formatted;
        info.appendChild(likes);

        if (!isReply && data.has_replies) {
            const div = document.createElement('div');
            const a = document.createElement('a');
            a.className = 'toggle-replies';
            a.setAttribute('data-reply-count', data.reply_count_formatted);
            div.appendChild(a);
            info.appendChild(div);
        }

        return info;
    }

    function createElement(data, isReply = false) {
        const element = document.createElement('div');
        element.className = isReply ? 'reply' : 'comment';
        element.id = data.comment_id;

        element.appendChild(createProfilePicture(data));
        element.appendChild(createAuthorInfo(data, isReply));
        element.appendChild(createBody(data));
        element.appendChild(createInfo(data, isReply));

        return element;
    }

    const commentBox = document.createElement('div');
    commentBox.className = 'comment-box';

    const comment = createElement(commentData);
    commentBox.appendChild(comment);

    if (commentData.replies && commentData.replies.length) {
        const repliesContainer = document.createElement('div');
        repliesContainer.className = 'replies hidden';

        commentData.replies.forEach(replyData => {
            const reply = createElement(replyData, true);
            repliesContainer.appendChild(reply);
        });

        commentBox.appendChild(repliesContainer);

        // add show replies button functionality
        const replyButtons = commentBox.querySelectorAll('.toggle-replies');
        initializeCollapsableReplies(replyButtons);
    }

    return commentBox;
}


class PageHandler {
    constructor(fetchUrl, parentElementId, buttonId) {
        this.fetchUrl = fetchUrl;
        this.parentElement = document.getElementById(parentElementId);
        this.button = document.getElementById(buttonId);
        this.pageToken = null;

        this.button.addEventListener('click', () => this.onNextPageButton());
    }

    hideButtonIfNeeded() {
        if (this.pageToken && this.pageToken.is_last_page) {
            this.button.classList.add("no-show");
        } else {
            this.button.classList.remove("no-show");
        }
    }

    createPage(data) {
        const page = document.createElement("div");
        page.className = "page";

        data.forEach(item => {
            const element = this.createElement(item);
            page.appendChild(element);
        });

        this.parentElement.appendChild(page);
    }

    processPage(pageData) {
        if (pageData.page == null) {
            console.log("it is null");
        } else {
            this.createPage(pageData.page);
            this.pageToken = pageData.page_token;
            this.hideButtonIfNeeded();
        }
    }

    fetchMoreData() {
        if (!this.pageToken || !this.pageToken.is_last_page) {
            fetch(this.fetchUrl, {
                method: 'GET',
                headers: { 'token': JSON.stringify(this.pageToken) }
            })
            .then(response => response.json())
            .then(data => this.processPage(data.data));
        }
    }

    onNextPageButton() {
	this.fetchMoreData();
    }
}

class PaginatedPageHandler extends PageHandler {
    constructor(fetchUrl, parentElementId, previousButtonId, nextButtonId, currentPageId) {
        super(fetchUrl, parentElementId, nextButtonId);

        this.previousButton = document.getElementById(previousButtonId);
        this.currentPageElement = document.getElementById(currentPageId);

        this.currentPageNum = 1;
        this.numPagesLoaded = 1;

        this.previousButton.addEventListener('click', () => this.onPreviousPageButton());
    }

    updateCurrentPageNum() {
        this.currentPageElement.textContent = this.currentPageNum;

        const pages = this.parentElement.children;
        Array.from(pages).forEach((page, index) => {
            if (index + 1 === this.currentPageNum) {
                page.classList.remove("hidden");
            } else {
                page.classList.add("hidden");
            }
        });

        this.hidePaginationArrows();
    }

    hidePaginationArrows() {
        if (this.currentPageNum <= 1) {
            this.previousButton.classList.add("no-show");
        } else {
            this.previousButton.classList.remove("no-show");
        }

        if (this.currentPageNum < this.numPagesLoaded || (this.currentPageNum === this.numPagesLoaded && !this.pageToken.is_last_page)) {
            this.button.classList.remove("no-show");
        } else {
            this.button.classList.add("no-show");
        }
    }

    onNextPageButton() {
        if (this.currentPageNum < this.numPagesLoaded) {
            this.currentPageNum++;
            this.updateCurrentPageNum();
        } else if (this.currentPageNum === this.numPagesLoaded && !this.pageToken.is_last_page) {
            this.fetchMoreData();
            this.numPagesLoaded++;
            this.currentPageNum = this.numPagesLoaded;
            this.updateCurrentPageNum();
        }
    }

    onPreviousPageButton() {
        if (this.currentPageNum > 1) {
            this.currentPageNum--;
            this.updateCurrentPageNum();
        }
    }
}

class VideoCommentsHandler extends PageHandler {
    constructor() {
        super('/data/get-comments', 'comments-section', 'fetchMoreCommentsButton');
    }

    createElement(commentData) {
        return createNewCommentsPage(commentData);
    }
}

class SearchResultsHandler extends PageHandler {
    constructor() {
        super('/data/get-search-results', 'videos', 'fetchMoreSearchResultsButton');
    }

    createElement(videoData) {
        return createVideoElement(videoData);
    }
}

class ChannelVideosHandler extends PaginatedPageHandler {
    constructor() {
        super('/data/get-channel-videos', 'video-feed', 'previousPageButton', 'nextPageButton', 'currentPageNum');
    }

    createElement(videoData) {
        return createVideoElement(videoData);
    }
}
