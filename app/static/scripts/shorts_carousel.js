var currentIndex = 0;
const numVideosDisplayed = 5;

var shortsCarousel = document.getElementById('shorts-carousel');
const shorts = shortsCarousel.querySelectorAll('.short-container');

function setShutter() {
    shorts.forEach(short => {
        short.classList.add('hidden');
    });

    for (let i = currentIndex; i < currentIndex + numVideosDisplayed && i < shorts.length; i++) {
        shorts[i].classList.remove('hidden');
    }
}

setShutter();
