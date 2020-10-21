import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import Nav from "./Nav";
import Lobby from "./components/Lobby";
import Login from "./components/Login";
import Signup from "./components/SignUp";
import Match from "./components/Match";
import CreateMatch from "./components/CreateMatch";


function App() {
  return (
    <BrowserRouter>
      <div className="App">
        <Nav />
        <Switch>
          <Route exact path="/" component={Lobby} />
          <Route exact path="/login" component={Login} />
          <Route exact path="/signup" component={Signup} />
          <Route exact path="/match/create" component={CreateMatch} />
          <Route exact path="/match/:id" component={Match} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;
