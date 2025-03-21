const container = document.getElementsByClassName('feed-container')[0];
const selector = document.getElementsByClassName('feed-selector')[0];

selector.addEventListener('click', (e) => {
    e.preventDefault();

    const currentTab = selector.querySelector('.active');

    if (e.target.tagName === 'A' && e.target !== currentTab) {
        container.className = 'feed-container ' + e.target.id;

        currentTab.classList.remove('active');
        e.target.classList.add('active');

        currentTab = e.target;
    }
});
