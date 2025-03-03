var currentIndex = 0;
const numVideosDisplayed = 5;

var shortsCarousel = document.getElementById('shorts-carousel');
const shorts = shortsCarousel.querySelectorAll('.short-container');
const leftArrow = document.getElementById('left-arrow');
const rightArrow = document.getElementById('right-arrow');

function setShutter() {
    shorts.forEach(short => {
        short.classList.add('hidden');
    });

    for (let i = currentIndex; i < currentIndex + numVideosDisplayed && i < shorts.length; i++) {
        shorts[i].classList.remove('hidden');
    }
}

function moveLeft() {
    if (currentIndex > 0) {
        currentIndex -= numVideosDisplayed;
        setShutter();
    }
}

function moveRight() {
    if (currentIndex < shorts.length - numVideosDisplayed) {
        currentIndex += numVideosDisplayed;
        setShutter();
    }
}

// starts the carousel at the first page
setShutter();

leftArrow.addEventListener('click', moveLeft);
rightArrow.addEventListener('click', moveRight);