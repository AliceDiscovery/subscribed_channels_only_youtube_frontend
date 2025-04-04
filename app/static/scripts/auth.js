const errorMessage = document.getElementById('errorMessage');
function setError(message) {
    errorMessage.innerText = message;
    errorMessage.className = '';
}

function signup() {
    alert('To be implemented...');
}
function login() {
    alert('To be implemented...');
}

function validateForm(email, password, password2) {
    function isEmail(str) {
        return /^[\w\-\.]+(\+[\w\-\.]+)?@([\w-]+\.)+[\w-]{2,}$/.test(str);
    }
    if (!email && !password) {
        setError('Please enter your email and password');
        return false;
    }
    if (!email) {
        setError('Please enter your email');
        return false;
    }
    if (!password) {
        setError('Please enter your password');
        return false;
    }
    if (!isEmail(email)) {
        setError('Invalid email address');
        return false;
    }
    if (password2 !== undefined) {
        if (!password2) {
            setError('Please re-enter your password');
            return false;
        }
        if (password !== password2) {
            setError('Passwords must be identical');
            return false;
        }
    }
    return true;
}

function submitHandler(e) {
    e.stopPropagation();
    e.preventDefault();
    errorMessage.className = 'hidden'
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
    const email = e.target[0].value;
    const password = e.target[1].value;
    const password2 = e.target[2].value;
    if (validateForm(email, password, password2)) signup(email, password);
});
