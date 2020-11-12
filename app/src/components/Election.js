import React from "react";
import { useSelector } from "react-redux";
import Vote from "./Vote";

function Election({ playerList, minister }) {
  const user = useSelector((state) => state.user);

  function getPlayerVote() {
    if (!playerList[user.username].isDead)
      return playerList[user.username].vote;
    return "";
  }

  return (
    <div>
      <h1>The current minister is {minister}</h1>
      {Object.entries(playerList).map((player) => (
        <h4>
          {player[1].isDead ? "" : player[0] + " voted " + player[1].vote}
        </h4>
      ))}
      <div>{getPlayerVote() === "missing vote" ? <Vote /> : ""}</div>
    </div>
  );
}
export default Election;
