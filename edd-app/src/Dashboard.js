// import logo from './logo.svg';
import './App.css';
import { db } from "./utils/firebase";
import { onValue, onChildAdded,ref, query, orderByChild } from "firebase/database"
import { useEffect, useState } from "react";
import SpeedGraph from './components/SpeedGraph';
import {auth, logout} from "./utils/firebase.js"
import { useAuthState } from "react-firebase-hooks/auth";
import { Link, useNavigate } from "react-router-dom";

function Dashboard() {

  const [devices, setDevices] = useState([]);

  const [user, loading, error] = useAuthState(auth);
  const navigate = useNavigate();

  useEffect(() => {
    if (loading) return;
    if (!user) return navigate("/");

    var pageQuery = query(ref(db, "users/" + user.uid + "/devices"), orderByChild('creation'));
    
    return onValue(pageQuery, (snapshot) => {

      var data = []

      if (snapshot.exists()) {
        snapshot.forEach((childSnapshot) => {
            var device = childSnapshot.val()
            device["deviceID"] = childSnapshot.key
            data.push(device)
          });
      }
      
      setDevices(data)

    //   console.log(snapshot.val())

    //   var tempTimes = []
    //   var tempSpeeds = []

    //   if(snapshot.exists()) {
    //     Object.values(data).map((entry) => {
    //       tempTimes = [...tempTimes, entry["date_time"]]
    //       tempSpeeds = [...tempSpeeds, entry["speed"]]
    //     })

    //     setTimes(tempTimes)
    //     setSpeeds(tempSpeeds)
    //   }
    
    })
  }, [user, loading]);

  // retrieve data whenever there is a change

  return (
    <div className="App">
      <header className="App-header">
        <p className="title">
          Dashboard
        </p>
        <div>
      {devices.map(data => (
        <button key={data.deviceID} onClick={logout}>
            <p>{data.deviceID}</p>
        </button>
      ))}
    </div>
        <button className="dashboard__btn" onClick={logout}>
          Logout
         </button>
      </header>
    </div>
  );
}

export default Dashboard;
