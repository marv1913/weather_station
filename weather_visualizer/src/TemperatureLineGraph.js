import React, {Component} from "react";
import {Button} from 'reactstrap';
import {GenerateLineGraph} from "./LineGraph";

class TemperatureLineGraph extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            data: [],
            uri: props.uri,
            valueCount: 144
        };
    }

    componentDidMount() {
        console.log(this.state.uri)
        fetch("http://192.168.178.123:5000/" + this.state.uri)
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        data: this.handleData({
                            data: result, key: this.state.key, key_sub_dict: this.state.key_sub_dict,
                            text_current_value: this.state.text_current_value
                        })
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


    SetDuration(duration) {
        let valueCount = 144
        switch (duration) {
            case 12:
                valueCount = valueCount / 2;
                break
            case 6:
                valueCount = valueCount / 4;
                break
            case 3:
                valueCount = valueCount / 8;
                break
        }
        this.setState({
            valueCount: valueCount
        });
    }

    render() {
        const {error, isLoaded} = this.state;
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return <div>
                <ul className="viewButtonList">
                    <li><Button className="viewButton" variant="contained" color="primary"
                                onClick={() => this.SetDuration(24)}>24 hours</Button></li>
                    <li><Button className="viewButton" variant="contained" color="primary"
                                onClick={() => this.SetDuration(12)}>12 hours</Button></li>
                    <li><Button className="viewButton" variant="contained" color="primary"
                                onClick={() => this.SetDuration(6)}>6 hours</Button></li>
                    <li><Button className="viewButton" variant="contained" color="primary"
                                onClick={() => this.SetDuration(3)}>3 hours</Button></li>
                </ul>
                <article className="canvas-container">
                {(
                    GenerateLineGraph({
                        text: this.state.data.current_value,
                        data: this.state.data.values,
                        labels: this.state.data.labels,
                        label: this.state.line_description,
                        count: this.state.valueCount
                    })
                )}
                </article>
            </div>
        }
    }
}


export default TemperatureLineGraph;
