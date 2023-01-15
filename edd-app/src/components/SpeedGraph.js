import React from "react";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, registerables } from 'chart.js';
ChartJS.register(...registerables);

function SpeedGraph({times, speeds}){
    const data = {
        labels: times,
        datasets:[{
            label: 'Speed',
            data: speeds,
            fill: false,
            borderColor: '#615D6C',
            tension: 0.1
        }]
    }
    return(
        <div class="chart-container">
            <p>Speed</p>
            <Line data = {data}>

            </Line>
        </div>
    )
    
}

export default SpeedGraph