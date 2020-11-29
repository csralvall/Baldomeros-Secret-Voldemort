import userEvent from "@testing-library/user-event";
import React, { useState } from "react";
import { useSelector } from "react-redux";
import "./css/LegislativeSession.css";

function Expelliarmus({ expelliarmus, minister, director }) {
  const matchID = useSelector((state) => state.match.id);
  const username = useSelector((state) => state.user.username);

  const castExpelliarmus = async (desition) => {
    const url = "http://127.0.0.1:8000";

    await fetch(
      url +
        `/game/${matchID}/board/expelliarmus?playername=${username}&minister-desition=${desition}`,
      {
        method: "PATCH",
      }
    )
      .then((response) => {
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Failed to cast the spell. Try again");
          } else {
            alert("Unknown Error.");
          }
        } else {
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  const ministerExpelliarmus = (
    <div>
      <button
        className="choose-proclamations-btn"
        onClick={() => {
          castExpelliarmus("expelliarmus");
        }}
      >
        Acept Expelliarmus
      </button>
      <button
        className="choose-proclamations-btn"
        onClick={() => {
          castExpelliarmus("");
        }}
      >
        Reject Expelliarmus
      </button>
    </div>
  );

  const directorExpelliarmus = (
    <div>
      <button
        className="choose-proclamations-btn"
        onClick={() => {
          castExpelliarmus("");
        }}
      >
        Request Expelliarmus
      </button>
    </div>
  );

  return (
    <div>
      {expelliarmus === "unlocked" && director === username
        ? directorExpelliarmus
        : ""}
      {expelliarmus === "minister stage" && minister === username
        ? ministerExpelliarmus
        : ""}
    </div>
  );
}
export default Expelliarmus;
