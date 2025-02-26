// Constants
characterMax = 200;
ellipsisString = '... ';
showMore = 'Show more';
showLess = 'Show less';

const root = document.getElementsByClassName('channel-description')[0];



// Extract and split description content

const description = root.innerHTML.trim().split(' ');
root.innerHTML = null;

let charCount = 0;
let visibleText = '';
while (description.length && description[0].length + charCount <= characterMax) {
    console.log(description[0])
    charCount += description[0].length;
    visibleText += description.shift() + ' ';
}
visibleText = visibleText.trimEnd();

let invisibleText = '';
for (word of description) {
    invisibleText += word + ' ';
}

if (invisibleText === '') {
    root.innerHTML = visibleText;
    throw new Error('Not an error; the description is just short enough to fit without hiding part of it.')
};


// Create new elements and add content

const visible = document.createElement('div');
visible.innerHTML = visibleText;
root.appendChild(visible);

const invisible = document.createElement('div');
invisible.innerHTML = invisibleText;
invisible.className = 'hidden';
root.appendChild(invisible);

const ellipsis = document.createElement('div');
ellipsis.innerHTML = ellipsisString;
root.appendChild(ellipsis);

const button = document.createElement('button');
button.innerHTML = showMore;

let hidden = true;
button.onclick = e => {
    e.preventDefault();
    if (!hidden) {
        invisible.className = 'hidden';
        ellipsis.className = '';
        button.innerHTML = showMore;
        hidden = true;
    }
    else {
        invisible.className = '';
        ellipsis.className = 'hidden';
        button.innerHTML = showLess;
        hidden = false;
    }
};

root.appendChild(button);