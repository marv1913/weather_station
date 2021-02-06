import React, {Component} from "react";
import {GenerateLineGraph} from "./LineGraph";

class Humidity extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            humidity: []
        };
    }

    fill_graph() {
        let newLabels = []
        let datasets = []
        let currentHumidity = ""
        for (let i = 0; i < this.state.humidity.length; i++) {
            let timestamp = Object.keys(this.state.humidity[i])[0]
            newLabels.push(timestamp)

            datasets.push(this.state.humidity[i][timestamp].humidity)
        }
        return GenerateLineGraph({
            text: "current humidity: " + this.state.humidity[this.state.humidity.length-1][Object.keys(this.state.humidity[this.state.humidity.length-1])[0]].humidity + "%",
            data: datasets,
            labels: newLabels,
            label: "humidity in %"
        })
    }

    componentDidMount() {
        fetch("http://217.160.29.142:5000/weather")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        humidity: result.temperatures
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
                this.fill_graph()
            );
        }
    }
}


export default Humidity;