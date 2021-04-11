import React, {Component} from "react";
import {GetTimestampAndValue} from "./LineGraph";
import TemperatureLineGraph from "./TemperatureLineGraph";

class Humidity extends TemperatureLineGraph {
    constructor(props) {
        super(props);
        this.handleData = GetTimestampAndValue.bind(this)
        this.state = {
            error: null,
            isLoaded: false,
            uri: "weather",
            key: "humidity",
            key_sub_dict: "humidity",
            text_current_value: "current humidity: $value$%",
            line_description: "humidity in %"
        };
    }
}

export default Humidity;