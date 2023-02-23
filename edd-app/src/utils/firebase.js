// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getDatabase, ref, query, get, set } from "firebase/database";
import {getAuth, signInWithPopup, GoogleAuthProvider, signOut} from "firebase/auth";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional

const firebaseConfig = {
    apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
    authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN,
    databaseURL: process.env.REACT_APP_FIREBASE_DATABASE_URL,
    projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
    storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.REACT_APP_FIREBASE_APP_ID,
    measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);

//get database
export const db = getDatabase(app);

//Enable Google Login
export const auth = getAuth(app);
const googleProvider = new GoogleAuthProvider();
export const signInWithGoogle = async () => {
  try {
    const res = await signInWithPopup(auth, googleProvider);
    const user = res.user;
    const userID = user.uid
    const dbref = ref(db, "users/" + userID );

    const userData = await get(query(dbref));
    console.log(userData)
    if (!userData.exists()) {
      await set(ref(db, 'users/' + userID), {
        name: user.displayName,
        email: user.email,
      });
    }
  } catch (err) {
    console.error(err);
    alert(err.message);
  }
};
// export const signInWithGoogle = () => {
//   signInWithPopup(auth, googleProvider).then((res) => {
//     console.log(res.user)
//   }).catch((error) => {
//     console.log(error.message)
//   })
// }

//allow signout
export const logout = () => {
  signOut(auth);
};


