// import logo from './logo.svg';
import './App.css';
import { db } from "./utils/firebase";
import { onValue, onChildAdded, ref, update } from "firebase/database"
import { useEffect, useState } from "react";
import SpeedGraph from './components/SpeedGraph';
import {auth, logout} from "./utils/firebase.js"
import { useAuthState } from "react-firebase-hooks/auth";
import { Link, useNavigate } from "react-router-dom";

import { TextField, Button } from '@mui/material';
import { height, maxHeight } from '@mui/system';

export default function Register() {


  const [user, loading, error] = useAuthState(auth);
  const navigate = useNavigate();


  useEffect(() => {
    if (loading) return;
    if (!user) return navigate("/");
  }, [user, loading]);

  const [inputs, setInputs] = useState({});

  const handleChange = (event) => {
    const name = event.target.name;
    const value = event.target.value;
    setInputs(values => ({...values, [name]: value}))
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    // alert(inputs);
    registerDevice(inputs.deviceUID)
  }

  const registerDevice = (deviceUID) => {
    const userID = user.uid
    const dbref = ref(db, "users/" + userID + "/devices/");
    const time = Math.floor(Date.now()/1000)
    update(dbref, {[deviceUID] : {creation: time, user: 0}})
      .then(() => {
        // Data saved successfully!
        alert("Device: " + deviceUID + " has been registered successfully. You are user 0. Returning to Dashboard");
        navigate("/dashboard/");
      })
      .catch((error) => {
        // The write failed...
        console.error(error);
        alert(error.message);
      });
  }


  return (
    <div className="App">
      <header className="App-header">
        <p className="title">
          Register
        </p>
        <form onSubmit={handleSubmit}>
      <TextField 
        type="text" 
        name="deviceUID" 
        variant="filled"
        value={inputs.deviceUID || ""} 
        onChange={handleChange}
        label="Enter your device ID:"
        style={{width:300}}
      />

      <Button type="submit" variant="contained" style={{height:55, marginLeft:30}}> Submit </Button>
    </form>

      </header>
    </div>
  );
}
