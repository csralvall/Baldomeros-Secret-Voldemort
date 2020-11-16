import React, { useState } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import "./css/LegislativeSession.css";
import phoenixProclamation from "../media/cards/phoenixProclamation.png";
import deathEaterProclamation from "../media/cards/deathEaterProclamation.png";

if (process.env.NODE_ENV === "test") {
  Modal.setAppElement("*");
} else {
  Modal.setAppElement("#root");
}

function Adivination({ hand }) {
  const game = useSelector((state) => state.match);
  const [open, setOpen] = useState(false);

  const endAdivination = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/game/${game.id}/board/adivination`, {
      method: "PATCH",
    })
      .then((response) => {
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Failed cast adivination, try again");
          } else {
            alert("Unknown Error.");
          }
        } else {
          setOpen(false);
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  const getProclamationImg = (proclamation) => {
    if (proclamation == "phoenix") {
      return phoenixProclamation;
    } else {
      return deathEaterProclamation;
    }
  };

  return (
    <div>
      <button
        className="choose-proclamations-btn"
        onClick={() => {
          setOpen(true);
        }}
      >
        Cast Adivination
      </button>
      <Modal
        isOpen={open}
        onRequestClose={() => {
          setOpen(false);
        }}
        closeTimeoutMS={200}
        style={{
          content: {
            top: "50%",
            left: "50%",
            right: "auto",
            bottom: "auto",
            marginRight: "-50%",
            transform: "translate(-50%, -50%)",
          },
        }}
      >
        <div className="proc-list">
          {hand.map((card, index) => (
            <img
              key={index}
              src={getProclamationImg(card)}
              className="not-selected-proc"
            />
          ))}
        </div>
        <div className="send-cards-btn-div">
          <button
            className="send-cards-btn"
            onClick={() => {
              endAdivination();
            }}
          >
            Done
          </button>
        </div>
      </Modal>
    </div>
  );
}

export default Adivination;
