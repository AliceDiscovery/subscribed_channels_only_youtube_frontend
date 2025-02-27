const container = document.getElementsByClassName('feed-container')[0];
const selector = document.getElementsByClassName('feed-selector')[0];
container.className = 'feed-container videos';

selector.children[0].disabled = true;
let currentTab = selector.children[0].className;
for (let button of selector.children) {
    button.onclick = e => {
        e.preventDefault();
        if (e.target.className !== currentTab) {
            container.className = 'feed-container ' + e.target.className;
            for (let btn of selector.children) {
                btn.disabled = false;
            }
            e.target.disabled = true;
            currentTab = e.target.className;
        }
    };
}
