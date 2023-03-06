import './App.css';
import { db } from "./utils/firebase";
import { onValue, onChildAdded,ref, query, orderByChild } from "firebase/database"
import { useEffect, useState } from "react";
import SpeedGraph from './components/SpeedGraph';
import {auth, logout} from "./utils/firebase.js"
import { useAuthState } from "react-firebase-hooks/auth";
import { Link, useNavigate, useLocation } from "react-router-dom";

import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import { Grid } from '@mui/material';

function Device() {
    const location = useLocation();
    const deviceData = location.state.data;

    const [sessions, setSessions] = useState([]);
    const [curSession, setCurSession]  = useState([]);

    useEffect(() => {
        var path = "devices/" + deviceData.deviceID + "/" + deviceData.user + "/sessions"
        var pageQuery = query(ref(db, "devices/" + deviceData.deviceID + "/" + deviceData.user + "/sessions"));
        console.log(path)
        return onValue(pageQuery, (snapshot) => {
            var data = []
            if (snapshot.exists()) {
                snapshot.forEach((childSnapshot) => {
                    var session = childSnapshot.val()
                    session["sessionID"] = childSnapshot.key
                    data.push(session)
                });
                console.log(data)
                setSessions(data)
                setCurSession('')
            } else {
                console.log("No data available")
            }
        })
    }, []);

    function SessionIncidentCards({data}) {
        //console.log(incs)
        if (data === '') {
            return <>Select a Session...</>;
        }
        console.log(data.incidents);
        if (!data.incidents) {
            return <>Incidents Unavailable</>
        }
        let incidents = Object.values(data.incidents);

        let speed_cnt = 0;
        let distracted_cnt = 0;
        let stop_blown_cnt = 0;
        for (var i = 0; i < incidents.length; i++){
            if (incidents[i].warning_type == 'speed')
                speed_cnt++;
            if (incidents[i].warning_type == 'distracted')
                distracted_cnt++;
            if (incidents[i].warning_type == 'stopBlown')
                stop_blown_cnt++;
        }
        console.log([speed_cnt, distracted_cnt, stop_blown_cnt])

        return (
            <div>
                <div >
                    Incidents Counts: <br></br>
                    Speed: {speed_cnt}, <br></br>
                    Distracted: {distracted_cnt}, <br></br>
                    Stop Signs Blown: {stop_blown_cnt} <br></br>
                </div>
                <Grid
                container
                spacing={2}
                direction="row"
                justify="flex-start"
                alignItems="flex-start"
                >
                    {incidents.map(inc => (
                        <Grid item xs={12} sm={6} md={3} key={incidents.indexOf(inc)}>
                            <IncidentCard inc={inc}></IncidentCard>
                        </Grid>
                    ))}
                </Grid>
            </div>
        );
    }

    function IncidentCard({inc}) {
        // console.log(inc)
        return (
          <Card sx={{ minWidth: 275 }} className="device-card">
            <CardContent>
            <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                {inc.date_time}
            </Typography>
            <Typography variant="h6" component="div">
                {inc.warning_type}
            </Typography>
            <Typography sx={{ fontSize: 14 }} color="text.secondary" gutterBottom>
                Inst. Speed: {Math.round(inc.speed * 100)/100} mph
            </Typography>
            </CardContent>
        </Card>
        );
    }

    const handleSessionSelect = (event) => {
        let session_name = event.target.value
        let session_id = 0
        for (var i = 0; i < sessions.length; i++){
            if (sessions[i]['sessionID'] === session_name){
                console.log("Current Session ID: " + i)
                session_id = i
                break;
            }
        }
        let curSessionObj = sessions[session_id]
        console.log(curSessionObj)
        setCurSession(curSessionObj);
    };

    return (
        <div className="App">
        <header className="Device-header">
            <div>
                <div className="device-title-container">
                    <p className="title">
                    Device ID: {deviceData.deviceID}
                    </p>
                </div>
                <div className="device-session-selector">
                    <Box sx={{ minWidth: 360 }}>
                    <FormControl fullWidth>
                        <InputLabel id="demo-simple-select-label">Session</InputLabel>
                        <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={curSession.sessionID}
                        label="Session"
                        onChange={handleSessionSelect}
                        >
                            {sessions.map(session => (
                                <MenuItem value={session.sessionID}>{session.sessionID}</MenuItem>
                            ))} 
                        </Select>
                    </FormControl>
                    </Box>
                </div>
            </div>
            <div>
                <SessionIncidentCards data={curSession}> </SessionIncidentCards>
            </div>

        </header>
              
        </div>
      );
}

export default Device;