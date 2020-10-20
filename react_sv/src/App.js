import React from 'react';
import './App.css';
import Login from "./components/login";
import {BrowserRouter as Router, Switch, Route} from "react-router-dom";

function App() {
  return (
    <Router>
      <div>
        <h1> Secret Voldemort </h1>
        <Login/>
      </div>
    </Router>
  );
}

export default App;
