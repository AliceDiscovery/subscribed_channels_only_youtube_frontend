const emailErrorMessage = document.getElementById('emailErrorMessage');
function setEmailError(message) {
    emailErrorMessage.innerText = message;
    emailErrorMessage.className = '';
}
const passwordErrorMessage = document.getElementById('passwordErrorMessage');
function setPasswordError(message) {
    passwordErrorMessage.innerText = message;
    passwordErrorMessage.className = '';
}
const password2ErrorMessage = document.getElementById('password2ErrorMessage');
function setPassword2Error(message) {
    password2ErrorMessage.innerText = message;
    password2ErrorMessage.className = '';
}


async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hash = await crypto.subtle.digest("SHA-256", data);
    return Array.from(new Uint8Array(hash))
                .map(b => b.toString(16).padStart(2, '0'))
                .join('');
}


async function signup(email, password) {
    const hashedPassword = await hashPassword(password);

    fetch("/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, password: hashedPassword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            setEmailError(data.error);
        } else {
            window.location.href = "/";
        }
    })
    .catch(error => console.error("Error:", error));
}

async function login(email, password) {
    const hashedPassword = await hashPassword(password);

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email, password: hashedPassword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            setEmailError(data.error);
        } else {
            window.location.href = "/";
        }
    })
    .catch(error => console.error("Error:", error));
}


function validateForm(email, password, password2) {
    function isEmail(str) {
        return /^[\w\-\.]+(\+[\w\-\.]+)?@([\w-]+\.)+[\w-]{2,}$/.test(str);
    }
    if (!email) {
        setEmailError('Please enter your email');
        return false;
    }
    if (!isEmail(email)) {
        setEmailError('Invalid email address');
        return false;
    }
    if (!password) {
        setPasswordError('Please enter your password');
        return false;
    }
    if (password2 !== undefined) {
        if (!password2) {
            setPassword2Error('Please re-enter your password');
            return false;
        }
        if (password !== password2) {
            setPassword2Error('Passwords must be identical');
            return false;
        }
    }
    return true;
}

function submitHandler(e) {
    e.stopPropagation();
    e.preventDefault();
    emailErrorMessage.className = 'hidden';
    passwordErrorMessage.className = 'hidden';
}

const loginForm = document.getElementById('loginForm');
if (loginForm) loginForm.addEventListener('submit', e => {
    submitHandler(e);
    const email = e.target[0].value;
    const password = e.target[1].value;
    if (validateForm(email, password)) login(email, password);
});

const signupForm = document.getElementById('signupForm');
if (signupForm) signupForm.addEventListener('submit', e => {
    submitHandler(e);
    password2ErrorMessage.className = 'hidden';
    const email = e.target[0].value;
    const password = e.target[1].value;
    const password2 = e.target[2].value;
    if (validateForm(email, password, password2)) signup(email, password);
});
