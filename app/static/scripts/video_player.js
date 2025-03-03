const root = document.getElementsByClassName('video-player')[0];
const img = root.getElementsByTagName('img')[0];
const iframe = root.getElementsByTagName('iframe')[0];
const button = root.getElementsByClassName('play-button')[0];

button.onclick = e => {
    img.className = 'hidden';
    button.className = 'hidden';
    iframe.hidden = false;
};
