import { auth } from "./firebase-config.js";
import {
    signInWithEmailAndPassword,
    GoogleAuthProvider,
    signInWithPopup,
} from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";

document.getElementById("loginBtn").onclick = () => {
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
    signInWithEmailAndPassword(auth, email, password)
        .then(() => alert("Logged in successfully!"))
        .catch((e) => alert(e.message));
};

document.getElementById("googleLogin").onclick = () => {
    const provider = new GoogleAuthProvider();
    signInWithPopup(auth, provider)
        .then(() => alert("Google login successful"))
        .catch((e) => alert(e.message));
};
