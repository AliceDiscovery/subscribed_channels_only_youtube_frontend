const emailErrorMessage = document.getElementById('emailErrorMessage');
function setEmailError(message) {
    if (emailErrorMessage) {
        emailErrorMessage.innerText = message;
        emailErrorMessage.className = '';
    }
}
const passwordErrorMessage = document.getElementById('passwordErrorMessage');
function setPasswordError(message) {
    if (passwordErrorMessage) {
        passwordErrorMessage.innerText = message;
        passwordErrorMessage.className = '';
    }
}
const passwordReentryErrorMessage = document.getElementById('password2ErrorMessage');
function setPasswordReentryError(message) {
    if (passwordReentryErrorMessage) {
        passwordReentryErrorMessage.innerText = message;
        passwordReentryErrorMessage.className = '';
    }
}


async function hashPassword(password) {
    const encoder = new TextEncoder();
    const data = encoder.encode(password);
    const hash = await crypto.subtle.digest("SHA-256", data);
    return Array.from(new Uint8Array(hash))
                .map(b => b.toString(16).padStart(2, '0'))
                .join('');
}


function redirectAfterLogin(defaultUrl='/profile') {
    const params = new URLSearchParams(window.location.search);
    const next = params.get('next');

    const destination = next || defaultUrl;
    window.location.href = destination;
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

async function changePassword(curPassword, newPassword) {
    const hashedCurPassword = await hashPassword(curPassword);
    const hashedNewPassword = await hashPassword(newPassword);

    fetch("/change-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ curPassword: hashedCurPassword, newPassword: hashedNewPassword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            setPasswordError(data.error);
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
            redirectAfterLogin();
        }
    })
    .catch(error => console.error("Error:", error));
}


function validateEmail(email) {
    const emailPattern = /^[\w\-\.]+(\+[\w\-\.]+)?@([\w-]+\.)+[\w-]{2,}$/;
    if (!email) {
        setEmailError('Please enter your email');
        return false;
    }
    if (!emailPattern.test(email)) {
        setEmailError('Invalid email address');
        return false;
    }
    return true;
}

function validatePassword(password) {
    if (!password) {
        setPasswordReentry('Please enter your password');
        return false;
    }
    return true;
}

function ValidateMatchingPasswords(password1, password2) {
    if (password2 === undefined) return true;
    if (!password2) {
        setPasswordReentryError('Please enter your password again');
        return false;
    }
    if (password1 !== password2) {
        setPasswordReentryError('The passwords are spelt different');
        return false;
    }
    return true;
}

function validateLoginForm(email, password) {
    return validateEmail(email) &&
           validatePassword(password);
}

function validateSignupForm(email, password, password2) {
    return validateEmail(email) &&
           validatePassword(password) &&
           ValidateMatchingPasswords(password, password2);
}

function validateChangePasswordForm(curPassword, newPassword, newPassword2) {
    return validatePassword(curPassword) &&
            validatePassword(newPassword) &&
            ValidateMatchingPasswords(newPassword, newPassword2);
}


function submitHandler(e) {
    e.stopPropagation();
    e.preventDefault();
    emailErrorMessage?.classList?.add('hidden');
    passwordErrorMessage?.classList?.add('hidden');
    passwordReentryErrorMessage?.classList.add('hidden');
}

const loginForm = document.getElementById('loginForm');
if (loginForm) loginForm.addEventListener('submit', e => {
    submitHandler(e);
    const email = e.target[0].value;
    const password = e.target[1].value;
    if (validateLoginForm(email, password)) login(email, password);
});

const signupForm = document.getElementById('signupForm');
if (signupForm) signupForm.addEventListener('submit', e => {
    submitHandler(e);
    const email = e.target[0].value;
    const password = e.target[1].value;
    const password2 = e.target[2].value;
    if (validateSignupForm(email, password, password2)) signup(email, password);
});

const changePasswordForm = document.getElementById("changePasswordForm");
if (changePasswordForm) changePasswordForm.addEventListener('submit', e => {
    submitHandler(e);
    const curPassword = e.target[0].value;
    const newPassword = e.target[1].value;
    const newPassword2 = e.target[2].value;

    if (validateChangePasswordForm(curPassword, newPassword, newPassword2)) {
        changePassword(curPassword, newPassword);
    }
});
