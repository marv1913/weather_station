import React, {Component} from "react";
import {Line} from 'react-chartjs-2';




class Particulates extends Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            data: [],
            pm_10: "",
            pm_25: ""
        };
    }

    get_current_temp() {
        let graph_data = []
        let data = {
            labels: [],
            datasets: [
                {
                    data: [],
                    fill: false,
                    backgroundColor: 'rgb(255, 99, 132)',
                    borderColor: 'rgba(255, 99, 132, 0.2)',
                    label: "pm 10"
                },
                {
                    data: [],
                    fill: false,
                    backgroundColor: 'rgb(255, 99, 200)',
                    borderColor: 'rgba(255, 99, 132, 0.2)',
                    label: "pm 25"
                }
            ]
        }

        data.datasets[0].data = []
        data.datasets[1].data = []
        data.labels = []
        for (let i = 0; i < this.state.data.length; i++) {
            data.labels.push(this.state.data[i].timestamp)
            data.datasets[0].data.push(this.state.data[i].pm_10)
        }
        for (let i = 0; i < this.state.data.length; i++) {
            data.labels.push(this.state.data[i].timestamp)
            data.datasets[1].data.push(this.state.data[i].pm_25)
        }
        graph_data.pm_10 = this.state.data[this.state.data.length - 1].pm_10
        graph_data.pm_25 = this.state.data[this.state.data.length - 1].pm_25

        graph_data.data = data
        return graph_data
    }

    get_pm_10(){
        let pm_10 = this.get_current_temp().pm_10
        let color = ""
        if(pm_10 < 20){
            color = "green"
        }else if(pm_10 < 35){
            color = "greenyellow"
        }else if(pm_10 < 50){
            color = "yellow"
        }
        else if(pm_10 < 100){
            color = "orange"
        }else{
            color = "red"
        }
        return <li style={{backgroundColor: color, fontSize: "x-large"}}>pm10:  {this.get_current_temp().pm_10}ppm</li>
    }

    get_pm_25(){
        let pm_25 = this.get_current_temp().pm_10
        let color = ""
        if(pm_25 < 12){
            color = "green"
        }else if(pm_25 < 35){
            color = "yellow"
        }
        else if(pm_25 < 55){
            color = "orange"
        }else{
            color = "red"
        }
        return <li style={{backgroundColor: color, fontSize: "x-large"}}>pm25:  {this.get_current_temp().pm_25}ppm</li>
    }

    componentDidMount() {
        fetch("http://192.168.178.123:5000/particulates")
            .then(res => res.json())
            .then(
                (result) => {
                    this.setState({
                        isLoaded: true,
                        data: result
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
            let graph_data = this.get_current_temp()
            return (

                <div>
                    <div id="menu">
                        <ul>
                            {this.get_pm_10()}
                            {this.get_pm_25()}
                        </ul>
                    </div>
                    <article className="canvas-container">
                    <Line
                        data={graph_data.data}
                        options={{
                            responsive: true,
                            maintainAspectRatio: false,
                            title: {
                                display: true,
                                fontSize: 20
                            },
                            scales: {
                                yAxes: [
                                    {
                                        ticks: {
                                            beginAtZero: true,
                                        }
                                    }
                                ],
                                xAxes: [
                                    {
                                        offset: true,
                                        ticks: {
                                            beginAtZero: true,
                                            autoSkip: true,
                                            maxTicksLimit: 25,

                                        }
                                    },
                                ],
                            }
                        }}
                    />
                    </article>
                </div>
            );
        }
    }
}


export default Particulates;