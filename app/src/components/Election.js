import React from "react";
import { useSelector } from "react-redux";
import Vote from "./Vote";
import LegislativeSession from "./LegislativeSession";
import Nomination from "./Nomination";
import "./css/Election.css";

function Election({ playerList, minister, director, candidate, status, hand }) {
  const user = useSelector((state) => state.user);

  function getPlayerVote() {
    if (!playerList[user.username].isDead)
      return playerList[user.username].vote;
    return "";
  }

  const DirectorNomination = (
    <div>
      <h1>Minister {minister} is nominating a Director...</h1>
      {minister === user.username ? <Nomination /> : ""}
    </div>
  );

  const VotingPhase = (
    <div>
      <h1>
        Minister {minister} nominated {candidate} to be Director
      </h1>
      {Object.entries(playerList).map((player) => (
        <h4 className="player-name-election">
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
      {status === "director selection" || status === "minister selection"
        ? ""
        : Object.entries(playerList).map((player) => (
            <h4 className="player-name-election">
              {player[1].isDead ? "" : player[0] + " voted " + player[1].vote}
            </h4>
          ))}
    </div>
  );

  return (
    <div>
      {status === "nomination" ? DirectorNomination : ""}
      {status === "election" ? VotingPhase : ""}
      {status === "minister selection" || status === "director selection"
        ? Session
        : ""}
    </div>
  );
}
export default Election;
