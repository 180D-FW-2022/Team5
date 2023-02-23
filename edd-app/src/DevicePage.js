// import logo from './logo.svg';
import './App.css';
import { db } from "./utils/firebase";
import { onValue, onChildAdded,ref, query, orderByChild } from "firebase/database"
import { useEffect, useState } from "react";
import {auth, logout} from "./utils/firebase.js"
import { useAuthState } from "react-firebase-hooks/auth";
import { Link, useLocation } from "react-router-dom";



function DevicePage() {
    const location = useLocation()
    const deviceData = location.state.data

    const [sessions, setSessions] = useState([]);
      

    useEffect(() => {

        var path = "devices/" + deviceData.deviceID + "/" + deviceData.user
    
        var pageQuery = query(ref(db, "devices/" + deviceData.deviceID + "/" + deviceData.user));

        console.log(path)
        
        return onValue(pageQuery, (snapshot) => {
    
          var data = snapshot.val()
    
          if (snapshot.exists()) {
            console.log(data)
          }
        
        })
      }, []);

  return (
    <div className="App">
      <header className="App-header">
        <p className="title">
          Device Info: {deviceData.deviceID}
        </p>
        <div>
      {/* {devices.map(data => (

        <DeviceButton key={data.deviceID} name ={data.deviceID} handleClick={deviceInfo}> </DeviceButton>
      ))} */}
      {/* <DeviceButton name ={"Register"} handleClick={register}> </DeviceButton> */}
    </div>
        <button className="logout_btn" onClick={logout}>
          Logout
         </button>
      </header>
          
    </div>
  );
}

export default DevicePage;
