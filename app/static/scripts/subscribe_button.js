const subscribeButton = document.getElementById('subscribe-button');

const buttonStates = ['subscribe', 'subscribed'];
const textStates = ['Subscribe', 'Subscribed'];


function toggle_subscribe_button() {
    if (subscribeButton.classList.contains(buttonStates[0])) {
        subscribeButton.classList.remove(buttonStates[0]);

        subscribeButton.classList.add(buttonStates[1]);
        subscribeButton.textContent = textStates[1];
    } else {
        subscribeButton.classList.remove(buttonStates[1]);
        subscribeButton.classList.add(buttonStates[0]);
        subscribeButton.textContent = textStates[0];
    }
}


subscribeButton.addEventListener('click', toggle_subscribe_button);