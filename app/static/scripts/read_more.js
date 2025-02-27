const characterMax = 200;

const ellipsisString = '... ';
const showMore = 'Show more';
const showLess = 'Show less';


function handleReadMore() {
    const root = document.getElementsByClassName('channel-description')[0];
    const description = root.innerHTML.trim().split(' ');
    root.innerHTML = '';

    const { visibleText, invisibleText } = truncateText(description);
    if (invisibleText.trim() === '') {
        root.innerHTML = visibleText;
    } else {
        createDescriptionElements(root, visibleText, invisibleText);
    }
}

function truncateText(description) {
    let charCount = 0;
    let visibleText = '';
    let invisibleText = '';

    while (description.length && description[0].length + charCount <= characterMax) {
        charCount += description[0].length;
        visibleText += description.shift() + ' ';
    }
    visibleText = visibleText.trimEnd();

    for (let word of description) {
        invisibleText += word + ' ';
    }

    return { visibleText, invisibleText };
}

function createDescriptionElements(root, visibleText, invisibleText) {
    const visible = createElement('div', visibleText);
    const invisible = createElement('div', invisibleText, 'hidden');
    const ellipsis = createElement('div', ellipsisString);
    const button = createElement('button', showMore);

    let hidden = true;
    button.onclick = e => {
        e.preventDefault();
        hidden = toggleVisibility(hidden, invisible, ellipsis, button);
    };

    root.appendChild(visible);
    root.appendChild(invisible);
    root.appendChild(ellipsis);
    root.appendChild(button);
}

function createElement(tag, content, className = '') {
    const element = document.createElement(tag);
    element.innerHTML = content;
    if (className) element.className = className;
    return element;
}

function toggleVisibility(hidden, invisible, ellipsis, button) {
    if (!hidden) {
        invisible.className = 'hidden';
        ellipsis.className = '';
        button.innerHTML = showMore;
    } else {
        invisible.className = '';
        ellipsis.className = 'hidden';
        button.innerHTML = showLess;
    }
    return !hidden;
}


handleReadMore();
