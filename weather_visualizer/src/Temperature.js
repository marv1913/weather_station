import React from "react";
import {GetTimestampAndValue} from "./LineGraph";
import TemperatureLineGraph from "./TemperatureLineGraph";

class Temperature extends TemperatureLineGraph {
    constructor(props) {
        super(props);
        this.handleData = GetTimestampAndValue.bind(this)
        this.state = {
            error: null,
            isLoaded: false,
            uri: "weather",
            key: "temperatures",
            key_sub_dict: "temperature",
            text_current_value: "current temperature: $value$°C"
        };
    }
}

export default Temperature;