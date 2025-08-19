import { initializeApp } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js";

const firebaseConfig = {
    apiKey: "AIzaSyDygdZ1VDPucOxUk7pQIPXK7QhkgBOp6fk",
    authDomain: "getsetcertified.firebaseapp.com",
    projectId: "getsetcertified",
    storageBucket: "getsetcertified.firebasestorage.app",
    messagingSenderId: "101229445369",
    appId: "1:101229445369:web:28f94272d6895fdba02228",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
