import React from 'react';
import { useSelector, useDispatch} from "react-redux";


function Match( {match} ) {

  const game = useSelector(state => state.match);
  const user = useSelector((state) => state.user);

  return (
    <div>
      {game.id == match.params.id ? 
      (<div>
      <h1> {game.name} </h1>
      <h4> Game id : {game.id} </h4>
      <h3> {user.id == game.hostid ? "You are the Host" : "" } </h3>
      </div>)
      :
      (<div> You didn't join this game </div>)}
    </div>
  );
}

export default Match;
