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
import { fontWeight } from '@mui/system';

import L from 'leaflet'
import { MapContainer, TileLayer, useMap, Marker, Popup, Polyline } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow
});

L.Marker.prototype.options.icon = DefaultIcon;

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
            <div>
                <SessionMap data={data}></SessionMap>
                return <>This session contained no incidents or incidents are not available</>
            </div>
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
                <SessionMap data={data}></SessionMap>
                <div className="inc-summary-container">
                    <span style={{fontSize: 20, fontWeight: 'bold'}}>Incidents Summary:</span> <br></br>
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

    function SessionMap({data}) {
        if (!data.gps){
            return <>No GPS data found</>
        }
        console.log(Object.values(data.gps));
        let gps_vals = Object.values(data.gps);
        let gps_route = {
            data: []
        }

        // Drawing a GPS polyline
        let polyline_id = 0;
        for (var i = 0; i < gps_vals.length - 1; i++) {
            let cur_line = {
                from_lat: gps_vals[i].lat,
                from_long: gps_vals[i].lon,
                id: polyline_id,
                to_lat: gps_vals[i+1].lat,
                to_long: gps_vals[i+1].lon
            }
            polyline_id++;
            gps_route.data.push(cur_line);
        }

        console.log(gps_route);

        return (
            <div className="map-outer-container">
            <MapContainer center={[34.082237, -118.443598]} style={{ width: "100%", height: "100%" }} zoom={11} scrollWheelZoom={false}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {gps_route.data.map(({id, from_lat, from_long, to_lat, to_long}) => {
                return <Polyline key={id} positions={[
                [from_lat, from_long], [to_lat, to_long],
                ]} color={'red'} />
            })}
            <Marker position={[51.505, -0.09]}>
                <Popup>
                A pretty CSS3 popup. <br /> Easily customizable.
                </Popup>
            </Marker>
            </MapContainer>
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
            <div className='device-title-selector-container'>
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
            <div className='incidents-container'>
                <SessionIncidentCards data={curSession}> </SessionIncidentCards>
            </div>

        </header>
              
        </div>
      );
}

export default Device;