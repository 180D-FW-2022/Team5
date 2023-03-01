// import logo from './logo.svg';
import './App.css';
import Device from './Device'

import { BrowserRouter, Routes, Route } from "react-router-dom";
import { db } from "./utils/firebase";
import { onValue, onChildAdded,ref, query, orderByChild } from "firebase/database"
import { useEffect, useState } from "react";
import SpeedGraph from './components/SpeedGraph';
import {auth, logout} from "./utils/firebase.js"
import { useAuthState } from "react-firebase-hooks/auth";
import { Link, useNavigate } from "react-router-dom";

import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { Grid } from '@mui/material';


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

  function DeviceCard({data}) {
    const deviceInfo = () => {
      return navigate("/devices/" + data.deviceID, {state: {data: data}});
    };

    return (
      <Card sx={{ minWidth: 275 }} className="device-card">
        <CardContent>
          <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
            {data.deviceID}
          </Typography>
        </CardContent>
        <CardActions>
          <Button size="small" onClick={deviceInfo}> Details </Button>
        </CardActions>
      </Card>
    );
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
        <Grid
          container
          spacing={2}
          direction="row"
          justify="flex-start"
          alignItems="flex-start"
        >
            {devices.map(data => (
              <Grid item xs={12} sm={6} md={3} key={devices.indexOf(data)}>
                <DeviceCard data ={data}> </DeviceCard>
              </Grid>
        ))}
        </Grid>
    </div>
      </header>
          
    </div>
  );
}

export default Dashboard;
