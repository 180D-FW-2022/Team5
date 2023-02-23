// import logo from './logo.svg';
import './App.css';
import { db } from "./utils/firebase";
import { onValue, onChildAdded,ref } from "firebase/database"
import { useEffect, useState } from "react";
import SpeedGraph from './components/SpeedGraph';
import {auth, logout} from "./utils/firebase.js"
import { useAuthState } from "react-firebase-hooks/auth";
import { Link, useNavigate } from "react-router-dom";

function Data() {

  const [times, setTimes] = useState([]);
  const [speeds, setSpeeds] = useState([]);

  const [user, loading, error] = useAuthState(auth);
  const navigate = useNavigate();
// retrieve data whenever there is a change
  useEffect(() => {
    const query = ref(db, "User1/Time/");
    return onValue(query, (snapshot) => {
      const data = snapshot.val();

      var tempTimes = []
      var tempSpeeds = []

      if(snapshot.exists()) {
        Object.values(data).map((entry) => {
          tempTimes = [...tempTimes, entry["date_time"]]
          tempSpeeds = [...tempSpeeds, entry["speed"]]
        })

        setTimes(tempTimes)
        setSpeeds(tempSpeeds)
      }
    })
  }, [])

  useEffect(() => {
    if (loading) return;
    if (!user) return navigate("/");
  }, [user, loading]);

  return (
    <div className="App">
      <header className="App-header">
        <p className="title">
          Driver's Edd
        </p>
        <button className="dashboard__btn" onClick={logout}>
          Logout
         </button>
        <div className='Graph-Container'>
        <SpeedGraph times={times} speeds={speeds}></SpeedGraph>
      </div>
      </header>
    </div>
  );
}

export default Data;
