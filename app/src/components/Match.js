import React from 'react';
import { useSelector, useDispatch} from "react-redux";


function Match( {match} ) {

  const game = useSelector(state => state.match);

  return (
    <div>
      {game.id == match.params.id ? 
      (<div>
      <h1> {game.name} </h1>
      <h2> There are {game.userlist.length} players connected</h2>
      <h4> Game id : {game.id} </h4>
      </div>)
      :
      (<div> You didn't join this game </div>)}
    </div>
  );
}

export default Match;
