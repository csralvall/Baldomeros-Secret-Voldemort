import React from "react";
import JoinMatch from "./JoinMatch";
import { Link } from "react-router-dom";
import { useSelector } from "react-redux";

function Lobby() {
  const user = useSelector((state) => state.user);

  return (
    <div>
      {user.logged_in ? (
        <div>
          <h1> Welcome, {user.username} </h1>
          <Link to="/match/create">
            <button>Create Game</button>
          </Link>
          <JoinMatch />
        </div>
      ) : (
        <div>
          <h1> You are not Logged In</h1>
          <Link to="/login">
            <h1> Login</h1>
          </Link>
        </div>
      )}
    </div>
  );
}

export default Lobby;
