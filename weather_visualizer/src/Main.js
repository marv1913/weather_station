import React, { Component } from "react";
import {
    Route,
    NavLink,
    HashRouter
} from "react-router-dom";
import Home from "./Home";
import Rainfall from "./Rainfall";
import Temperature from "./Temperature";
import Humidity from "./Humidity";



class Main extends Component {
    render() {
        return (
            <HashRouter>
                <div>
                    <h1>Weather Station</h1>
                    <ul className="header">
                        <li><NavLink exact to="/">Home</NavLink></li>
                        <li><NavLink to="/rain">Rainfall</NavLink></li>
                        <li><NavLink to="/temperature">Temperature</NavLink></li>
                        <li><NavLink to="/humidity">Humidity</NavLink></li>
                        {/*<li><NavLink to="/contact">Contact</NavLink></li>*/}
                    </ul>
                    <div className="content">
                        <Route exact path="/" component={Home}/>
                        <Route path="/rain" component={Rainfall}/>
                        <Route path="/temperature" component={Temperature}/>
                        <Route path="/humidity" component={Humidity}/>
                        {/*<Route path="/contact" component={Contact}/>*/}
                    </div>
                </div>
            </HashRouter>
        );
    }
}



export default Main;