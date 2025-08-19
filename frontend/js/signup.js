import { auth } from './firebase-config.js';
import { createUserWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js';

document.getElementById('signupBtn').onclick = () => {
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirm = document.getElementById('signupConfirm').value;

    if (password !== confirm) return alert("Passwords don't match");

    createUserWithEmailAndPassword(auth, email, password)
    .then(() => alert('Signup successful!'))
    .catch(e => alert(e.message));
};

document.getElementById('googleSignup').onclick = () => {
    const provider = new GoogleAuthProvider();
    signInWithPopup(auth, provider)
    .then(() => alert('Google signup successful'))
    .catch(e => alert(e.message));
};