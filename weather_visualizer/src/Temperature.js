import React, {Component} from "react";
import {Line} from 'react-chartjs-2';

let data = {
    labels: [],
    datasets: [
        {
            label: 'temperature in °C',
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


class Temperature extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            temperatures: []
        };
    }

    get_current_temp() {
        data.datasets[0].data = []
        data.labels = []
        for (let i = 0; i < this.state.temperatures.length; i++) {
            let timestamp = Object.keys(this.state.temperatures[i])[0]
            data.labels.push(timestamp)

            data.datasets[0].data.push(this.state.temperatures[i][timestamp].temperature)
        }
        options.title.text = "current temperature: " + this.state.temperatures[0][Object.keys(this.state.temperatures[0])[0]].temperature + " °C"
        return data
    }

    componentDidMount() {
        fetch("http://217.160.29.142:5000/weather")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        temperatures: result.temperatures
                    });
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            )
    }

    render() {
        const {error, isLoaded} = this.state;
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <div>
                    <Line
                        data={this.get_current_temp()}
                        options={options}
                        height={80}
                    />
                </div>
            );
        }
    }
}


export default Temperature;
