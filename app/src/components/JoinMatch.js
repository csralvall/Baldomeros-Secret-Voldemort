import React from 'react';
import { useHistory } from "react-router-dom";
import { useDispatch } from "react-redux";
import { joinMatch } from "../actions/match"


function JoinMatch() {

    const dispatch = useDispatch();
    const history = useHistory(); 
    
    const user = { username: "Tom Riddle", id: 1, autenticator: true };
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
            .then(async (response) => {
                const responseData = await response.json
                if (!response.ok) {
                    if (response.status === 409) {
                        alert("");
                    } else {
                        alert("Could not join. Unknown Error.");
                    }
                } else {
                    dispatch(joinMatch(responseData));
                    history.push("/match/" + responseData.id);
                }
            })
            .catch(() => {
                alert("Network Error");
            });
    }
    return (
        <button onClick={() => { joinGame() }}>Join Game</button>
    )
}

export default JoinMatch;