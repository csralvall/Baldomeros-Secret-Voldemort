import React from 'react';

function Match( {match} ) {

  const game = {name : "Tom riddle's game",
                id : match.params.id,
                playerCount : 6};

  return (
    <div >
      <h1> {game.name} </h1>
      <h2> There are {game.playerCount} players connected</h2>
      <h4> Game id : {game.id} </h4>
    </div>
  );
}

export default Match;
