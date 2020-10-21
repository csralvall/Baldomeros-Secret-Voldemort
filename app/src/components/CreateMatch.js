import React, { useState } from "react";
import "./CreateMatch.css";

function CreateMatch() {
  const [matchProps, setMatchProps] = useState({
    minPlayers: 5,
    maxPlayers: 10,
  });

  const updateMinPlayers = (e) => {
    setMatchProps({
      minPlayers: parseInt(e.target.value),
      maxPlayers: matchProps.maxPlayers,
    });
  };

  const updateMaxPlayers = (e) => {
    setMatchProps({
      minPlayers: matchProps.minPlayers,
      maxPlayers: parseInt(e.target.value),
    });
  };

  const getMatchProps = (e) => {
    e.preventDefault();
    if (matchProps.minPlayers > matchProps.maxPlayers) {
      alert("Min players can't be larger than max players!");
    } else {
      console.log(matchProps);
    }
  };

  return (
    <div>
      <h1 className="title">Create Match</h1>
      <form onSubmit={getMatchProps} className="create-game-form">
        <label>
          Min Players
          <input
            min="5"
            max="10"
            className="text-input"
            type="number"
            value={matchProps.minPlayers}
            onChange={updateMinPlayers}
            required
          />
        </label>
        <label>
          Max Players
          <input
            min="5"
            max="10"
            className="text-input"
            type="number"
            value={matchProps.maxPlayers}
            onChange={updateMaxPlayers}
            required
          />
        </label>
        <button className="create-button" type="submit">
          Create Game
        </button>
      </form>
    </div>
  );
}

export default CreateMatch;
