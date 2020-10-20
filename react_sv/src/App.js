import React from 'react';
import './App.css';
import Login from "./components/login";
import Register from "./components/register";
import Lobby from "./components/Lobby";
import Home from "./components/Home";
import Match from "./components/Match";
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";

function App() {
  return (
    <Router>
      <div>
        <h1> Secret Voldemort </h1>
        <Route path="/" exact component = {Home}/>
        <Route path="/register" component = {Register}/>
        <Route path="/match" exact component = {Lobby}/>
        <Route path="/match/:id" component = {Match}/>
      </div>
    </Router>
  );
}

export default App;
