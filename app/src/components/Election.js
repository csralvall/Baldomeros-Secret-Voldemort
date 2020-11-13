import React from "react";
import { useSelector } from "react-redux";
import Vote from "./Vote";
import LegislativeSession from "./LegislativeSession";

function Election({ playerList, minister, director, status, hand }) {
  const user = useSelector((state) => state.user);

  function getPlayerVote() {
    if (!playerList[user.username].isDead)
      return playerList[user.username].vote;
    return "";
  }

  //This has to be a diferent component
  const Nomination = (
    <div>
      <h1>Minister {minister} is nominating a Director...</h1>
    </div>
  );

  const VotingPhase = (
    <div>
      <h1>
        Minister {minister} nominated {director} to be Director
      </h1>
      {Object.entries(playerList).map((player) => (
        <h4>
          {player[1].vote === "missing vote"
            ? player[0] + " is voting"
            : player[0] + " voted"}
        </h4>
      ))}
      {getPlayerVote() === "missing vote" ? <Vote /> : ""}
    </div>
  );

  const Session = (
    <div>
      <h1>
        {status === "director selection"
          ? "Director is choosing proclamations"
          : "Minister is choosing proclamations"}
      </h1>
      {(director === user.username && status === "director selection") ||
      (minister === user.username && status === "minister selection") ? (
        <LegislativeSession hand={hand} />
      ) : (
        ""
      )}
      {Object.entries(playerList).map((player) => (
        <h4>
          {player[1].isDead ? "" : player[0] + " voted " + player[1].vote}
        </h4>
      ))}
    </div>
  );

  return (
    <div>
      {status === "nomination" ? Nomination : ""}
      {status === "election" ? VotingPhase : ""}
      {status === "minister selection" || status === "director selection"
        ? Session
        : ""}
    </div>
  );
}
export default Election;
