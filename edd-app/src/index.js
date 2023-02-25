import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import Data from './Data';
import Login from './Login';
import Dashboard from "./Dashboard"
import Register from "./Register";
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import DevicePage from "./DevicePage"

export default function App() {
  return (
    <BrowserRouter basename={window.location.pathname || ''}>
      <Routes>
        <Route exact path="/" element={<Login />}/>
        <Route exact path="/dashboard" element={<Dashboard />}>
        </Route>
        <Route exact path="device-info" element={<DevicePage />}/>
        <Route exact path="/register" element={<Register />}/>
    
      </Routes>
    </BrowserRouter>
  );
}
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
