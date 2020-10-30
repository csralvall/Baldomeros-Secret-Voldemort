import React from 'react';
import { useHistory } from "react-router-dom";
import { useDispatch, useSelector } from "react-redux";
import { joinMatch } from "../actions/match"


function JoinMatch() {

    const dispatch = useDispatch();
    const history = useHistory();
    const user = useSelector((state) => state.user)
    const joinGame = async () => {
        const url = "http://127.0.0.1:8000";

        // const formData = new FormData();
        // formData.append("username", user.username);
        // formData.append("userid", user.id);
        // formData.append("autenticator", user.autenticator);
        // formData.append("matchid", 1);

        await fetch(url + "/game/1?user=" +user.id , {
            method: "POST",
            //body: formData,
        })
            .then(async (response) => {
                const responseData = await response.json()
                if (response.status !== 200) {
                    if (response.status === 404) {
                        alert("Could not join");
                    } else {
                        alert("Could not join. Unknown Error.");
                    }
                } else {
                    dispatch(joinMatch(responseData));
                    history.push("/match/" + responseData.Match_id);
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