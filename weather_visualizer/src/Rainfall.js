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
            let timestamp = Object.keys(this.state.rain[i])[0]
            data.labels.push(timestamp)
            data.datasets[0].data.push(this.state.rain[i][timestamp].sum_1)
        }
        return this.state.rain[0][Object.keys(this.state.rain[0])[0]].sum_24
    }

    componentDidMount() {
        fetch("http://217.160.29.142:5000/weather")
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
