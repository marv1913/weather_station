import React, {Component} from "react";
import {Line} from "react-chartjs-2";

let data = {
    labels: [],
    datasets: [
        {

            data: [],
            fill: false,
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgba(255, 99, 132, 0.2)',
        },
    ],
}

let options = {
    title: {
        display: true,
        text: "",
        fontSize: 20
    },
    scales: {
        yAxes: [
            {
                ticks: {
                    beginAtZero: true,
                },
            },
        ],
    },
}

export function GenerateLineGraph(props){
    options.title.text = props.text
    data.labels = props.labels
    data.datasets[0].data = props.data
    data.datasets[0].label = props.label
    return <div>
        <Line
            data={data}
            options={options}
            height={80}
        />
    </div>
}
