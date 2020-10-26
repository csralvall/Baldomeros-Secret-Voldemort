import React from 'react';
import {useHistory, Link} from "react-router-dom";
import { useSelector, useDispatch} from "react-redux";
import {joinMatch} from "./../actions/match"

function Lobby() {


  //Esto vendría de useSelector
  const user = {username:"Tom Riddle",id:1,autenticator:true};
  const logged_in = useSelector((state) => state.logged_in);
  const dispatch = useDispatch()

  const history = useHistory(); 

  const joinGame = async () => {
    const url = "http://127.0.0.1:8000";

    const formData = new FormData();
    formData.append("username", user.username);
    formData.append("userid", user.id);
    formData.append("autenticator", user.autenticator);
    const response = await fetch(url + "/match", {
      method: "GET",
      parameters: formData,
    })
      .then((response) => {
        const responseData = response.body.json
        if (!response.ok) {
          if (response.status === 409) {
            alert("");
          } else {
            alert("Could not join. Unknown Error.");
          }
        } else {
          dispatch(joinMatch(responseData));
          history.push("/match/"+responseData.id);
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  }

  return (
    <div> { logged_in ?
      (<div >
        <h1> Welcome, {user.username} </h1>
        <button>Create Game</button>
        <button onClick={() => {joinGame()}}>Join Game</button>
      </div>)

      :

      (<div>
        <h1> You are not Logged In</h1>
        <Link to = "/login" >
        <h1> Login</h1>
        </Link>
      </div>)
      }
    </div>
  );
}

export default Lobby;
