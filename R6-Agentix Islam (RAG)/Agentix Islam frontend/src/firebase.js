import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyC3qflJ2gy6QkuIDmcPPjes_ZytT_qlU2o",
    authDomain: "agentix-islam.firebaseapp.com",
    projectId: "agentix-islam",
    storageBucket: "agentix-islam.firebasestorage.app",
    messagingSenderId: "364166555344",
    appId: "1:364166555344:web:65e884ef3cebb36cb2a0d5",
    measurementId: "G-MP7B946JX4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

export { app, auth, provider };
