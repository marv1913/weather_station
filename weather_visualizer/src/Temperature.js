import React, {Component} from "react";
import {GenerateLineGraph} from "./LineGraph";

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
        let newLabels = []
        let datasets = []
        for (let i = 0; i < this.state.temperatures.length; i++) {
            let timestamp = Object.keys(this.state.temperatures[i])[0]
            newLabels.push(timestamp)

            datasets.push(this.state.temperatures[i][timestamp].temperature)
        }
        return GenerateLineGraph({
            text: "current temperature: " + this.state.temperatures[this.state.temperatures.length - 1]
                [Object.keys(this.state.temperatures[this.state.temperatures.length - 1])[0]].temperature,
            data: datasets,
            labels: newLabels,
            label: "temperature in °C"
        })
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
                this.get_current_temp()
            );
        }
    }
}


export default Temperature;
