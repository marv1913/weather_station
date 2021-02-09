import React from "react";
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

function LimitShownValues(props) {
    let newData = {}
    let startIndex = props.data.length - props.count;
    if (startIndex < 0) {
        startIndex = 0
    }
    newData.data = props.data.slice(startIndex, props.data.length)
    newData.labels = props.labels.slice(startIndex, props.labels.length)
    return newData

}

export function GenerateLineGraph(props) {
    options.title.text = props.text

    let limitedData = LimitShownValues({count: props.count, data: props.data, labels: props.labels})
    data.datasets[0].data = limitedData.data
    data.labels = limitedData.labels
    data.datasets[0].label = "text"
    return <Line
        data={data}
        options={options}
        height={80}
    />
}


export function GetTimestampAndValue(props) {
    let weather_array = props.data[props.key.toString()]
    let weather_data = {labels: [], values: [], current_value: null}

    for (let i = 0; i < weather_array.length; i++) {
        weather_data.labels.push(weather_array[i].timestamp)
        weather_data.values.push(weather_array[i][props.key_sub_dict])
    }
    let value = weather_array[weather_array.length - 1][props.key_sub_dict]
    weather_data.current_value = props.text_current_value.replace("$value$", value)
    console.log(weather_data)
    return weather_data
}
