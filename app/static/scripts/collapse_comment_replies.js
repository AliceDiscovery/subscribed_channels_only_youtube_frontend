var toggleButtons = document.querySelectorAll('.toggle-replies');


function findRepliesDiv(button) {
  let parent = button;
  while (parent && !parent.querySelector('.replies')) {
    parent = parent.parentNode;
  }
  return parent ? parent.querySelector('.replies') : null;
}

function updateButtonText(button) {
    var replyCount = button.getAttribute('data-reply-count');
    var showText = replyCount == 1 ? 'Show reply' : `show ${replyCount} replies`;
    var hideText = replyCount == 1 ? 'Hide reply' : `hide ${replyCount} replies`;
    button.textContent = findRepliesDiv(button).classList.contains('hidden') ? showText : hideText;
}

function toggleReplies(event) {
    event.preventDefault();
    var button = event.target;

    findRepliesDiv(button).classList.toggle('hidden');
    updateButtonText(button);
}

function initializeCollapsableReplies(buttons) {
    buttons.forEach(function (button) {
        updateButtonText(button);
        button.addEventListener('click', toggleReplies);
    });
}

initializeCollapsableReplies(toggleButtons);
