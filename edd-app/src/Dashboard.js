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

  function DeviceButton({data}){

    const deviceInfo = () => {
      return navigate("/device-info", {state: {data: data}});
    };
  
    return(
        <button onClick={deviceInfo}>
            <p>{data.deviceID}</p>
        </button>
    )
    
  }
  
  function RegisterButton ({data}){
  
    const deviceInfo = () => {
      return navigate("/device-info", {state: {data: data}});
    };
  
    const register = () => {
      return navigate("/register");
    };
  
    return(
        <button onClick={register}>
            <p>Register</p>
        </button>
    )
    
  }

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
      console.log(data)
      setDevices(data)
    
    })
  }, [user, loading]);

  

  return (
    <div className="App">
      <header className="App-header">
        <p className="title">
          Dashboard
        </p>
        <div>
      {devices.map(data => (

        <DeviceButton key={data.deviceID} data ={data}> </DeviceButton>
      ))}
      <RegisterButton> </RegisterButton>
    </div>
        <button className="logout_btn" onClick={logout}>
          Logout
         </button>
      </header>
          
    </div>
  );
}

export default Dashboard;
