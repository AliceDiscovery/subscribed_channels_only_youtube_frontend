var toggleButtons = document.querySelectorAll('.toggle-replies');

function updateButtonText(button, repliesDiv) {
    var replyCount = button.getAttribute('data-reply-count');
    var showText = replyCount == 1 ? `show reply...` : `show ${replyCount} replies...`;
    var hideText = replyCount == 1 ? `hide reply...` : `hide ${replyCount} replies...`;
    button.textContent = repliesDiv.classList.contains('hidden') ? showText : hideText;
}

function toggleReplies(event) {
    event.preventDefault();
    var button = event.target;
    var repliesDiv = button.parentNode.querySelector('.replies');

    repliesDiv.classList.toggle('hidden');
    updateButtonText(button, repliesDiv);
}

function initializeCollapsableReplies() {
    toggleButtons.forEach(function (button) {
        var repliesDiv = button.parentNode.querySelector('.replies');
        updateButtonText(button, repliesDiv);
        button.addEventListener('click', toggleReplies);
    });
}

initializeCollapsableReplies();
