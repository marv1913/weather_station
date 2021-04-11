import React, {Component} from "react";
import {Bar} from 'react-chartjs-2';


let data = {
    labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
    datasets: [{
        label: 'rain in mm per hour',
        data: [12, 19, 3, 5, 2, 3],
        backgroundColor:
            'rgba(255, 99, 132, 0.2)'
        ,
        borderColor:
            'rgba(255, 99, 132, 1)',

        borderWidth: 1
    }]
}

class Rainfall extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            rain: []
        };
    }

    get_current_temp() {
        data.datasets[0].data = []
        data.labels = []
        for (let i = 0; i < this.state.rain.length; i++) {
            data.labels.push(this.state.rain[i].timestamp)
            data.datasets[0].data.push(this.state.rain[i].sum_1)
        }
        return this.state.rain[this.state.rain.length - 1].sum_24
    }

    componentDidMount() {
        fetch("http://192.168.178.123:5000/weather")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        rain: result.rain
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
                    <Bar
                        data={data}
                        options={{
                            title: {
                                display: true,
                                text: "Sum last 24 hours: " + this.get_current_temp() + "mm",
                                fontSize: 20
                            },
                            legend: {
                                display: true,
                                position: 'right'
                            },
                            scales: {
                                yAxes: [{
                                    ticks: {
                                        beginAtZero:true,
                                        // min: 0,
                                        // max: 100
                                    }
                                }]
                            }
                        }}
                        height={80}
                    />
                </div>
            );
        }
    }
}


export default Rainfall;
