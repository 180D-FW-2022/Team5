import React from "react";
import {signInWithGoogle} from "./utils/firebase.js"
import GoogleButton from 'react-google-button'
import './App.css';

export default function Login() {
  return (
      <div className="App">
        <div className="App-header">
            <p className="title">
                Login
            </p>
            <GoogleButton onClick={signInWithGoogle}/>
        </div>
      </div>
  );
}