const subscribeButton = document.getElementById('subscribe-button');
const channelId = document.getElementById('subscribe-button').value;  // uses the `value` field to set the channelId


async function setSubscription(channelId, isSubscribed) {
    try {
        const res = await fetch(`/data/channel/${channelId}`, {
            method:  'POST',
            headers: {
            'Content-Type': 'application/json'
        },
        credentials: 'include',  // send cookies for @login_required
        body: JSON.stringify({ subscribed: isSubscribed })
    });

    if (!res.ok) {
        throw new Error(`HTTP ${res.status} – ${res.statusText}`);
    }

    const data = await res.json();
    return data;

    } catch (err) {
        console.error('Failed to update subscription:', err);
        throw err;
    }
}

async function getSubscription(channelId) {
    const res = await fetch(`/data/channel/${channelId}`, {
        method: 'GET',
        credentials: 'include'
    });
    if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
    }
    return res.json();
}


const buttonStates = ['notSubscribed', 'subscribed'];
const textStates = ['Subscribe', 'Subscribed'];

function toggleSubscribeButton() {
    if (subscribeButton.classList.contains(buttonStates[0])) {
        subscribeButton.classList.remove(buttonStates[0]);

        subscribeButton.classList.add(buttonStates[1]);
        subscribeButton.textContent = textStates[1];
        setSubscription(channelId, true)
    } else {
        subscribeButton.classList.remove(buttonStates[1]);
        subscribeButton.classList.add(buttonStates[0]);
        subscribeButton.textContent = textStates[0];
        setSubscription(channelId, false)
    }
}
subscribeButton.addEventListener('click', toggleSubscribeButton);
