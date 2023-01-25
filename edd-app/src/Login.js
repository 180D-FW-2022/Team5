import React, { useEffect } from "react";
import {signInWithGoogle, auth} from "./utils/firebase.js"
import { Link, useNavigate } from "react-router-dom";
import GoogleButton from 'react-google-button'
import './App.css';
import { useAuthState } from "react-firebase-hooks/auth";

export default function Login() {
  const [user, loading, error] = useAuthState(auth);
  const navigate = useNavigate();

  useEffect(() => {
    if (loading) {
      // maybe trigger a loading screen
      return;
    }
    if (user) navigate("/dashboard");
  }, [user, loading]);
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