// import logo from './logo.svg';
import './App.css';
import { db } from "./utils/firebase";
import { onValue, onChildAdded,ref } from "firebase/database"
import { useEffect, useState } from "react";
import SpeedGraph from './components/SpeedGraph';

function App() {

  const [times, setTimes] = useState([]);
  const [speeds, setSpeeds] = useState([]);
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

  return (
    <div className="App">
      <header className="App-header">
        <p className="title">
          Driver's Edd
        </p>
        <div className='Graph-Container'>
        <SpeedGraph times={times} speeds={speeds}></SpeedGraph>
      </div>
      </header>
    </div>
  );
}

export default App;
