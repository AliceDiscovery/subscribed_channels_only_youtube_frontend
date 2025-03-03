var currentIndex = 0;
var numShortsDisplayed;

const shortWidth = 225;
const marginSize = 50;

var shortsCarousel = document.getElementById('shorts-carousel');
const shorts = shortsCarousel.querySelectorAll('.short-container');
const leftArrow = document.getElementById('left-arrow');
const rightArrow = document.getElementById('right-arrow');

function setShutter() {
    shorts.forEach(short => {
        short.classList.add('hidden');
    });

    for (let i = currentIndex; i < currentIndex + numShortsDisplayed && i < shorts.length; i++) {
        shorts[i].classList.remove('hidden');
    }
}

function moveLeft() {
    if (currentIndex > 0) {
        currentIndex -= numShortsDisplayed;
        setShutter();
    }
}

function moveRight() {
    if (currentIndex < shorts.length - numShortsDisplayed) {
        currentIndex += numShortsDisplayed;
        setShutter();
    }
}

function updateNumShortsDisplayed() {
    const carouselWidth = shortsCarousel.offsetWidth;
    numShortsDisplayed = Math.max(1, Math.floor(carouselWidth / (shortWidth + marginSize)));
    setShutter();
}

// Update the number of shorts being displayed when the window resizes
window.addEventListener('resize', updateNumShortsDisplayed);

// Start the carousel at the first page
updateNumShortsDisplayed();

leftArrow.addEventListener('click', moveLeft);
rightArrow.addEventListener('click', moveRight);
