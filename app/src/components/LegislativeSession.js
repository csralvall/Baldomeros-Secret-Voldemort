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

function LegislativeSession({ hand }) {
  const user = useSelector((state) => state.user);
  const game = useSelector((state) => state.match);
  const [cardPool, setCardPool] = useState([false, false, false]);
  const [open, setOpen] = useState(false);

  function enableCard(index) {
    const cardsElected = cardPool;
    cardsElected[index] = !cardsElected[index];
    if (cardsElected.filter(Boolean).length <= hand.length - 1)
      setCardPool(cardsElected);
    else {
      cardsElected[index] = !cardsElected[index];
      alert("You cant choose more than " + (hand.length - 1) + " cards");
    }
  }

  const sendLegislativeSession = async () => {
    const url = "http://127.0.0.1:8000";
    const discarded = hand.find((card, index) => !cardPool[index]);
    const selected = hand.filter((card, index) => cardPool[index]);
    await fetch(
      url +
        `/game/${game.id}/proclamation/${game.playerId}?discarded=${discarded}`,
      {
        method: "POST",
        body: JSON.stringify(selected),
      }
    )
      .then((response) => {
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Failed to submit cards, try again");
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
        Choose Proclamations
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
              onClick={() => {
                enableCard(index);
              }}
              src={getProclamationImg(card)}
              className={
                cardPool[index] ? "selected-proc" : "not-selected-proc"
              }
            />
          ))}
        </div>
        {cardPool.filter(Boolean).length === hand.length - 1 ? (
          <div className="send-cards-btn-div">
            <button
              className="send-cards-btn"
              onClick={() => {
                sendLegislativeSession();
              }}
            >
              Send Cards
            </button>
          </div>
        ) : (
          ""
        )}
      </Modal>
    </div>
  );
}

export default LegislativeSession;
