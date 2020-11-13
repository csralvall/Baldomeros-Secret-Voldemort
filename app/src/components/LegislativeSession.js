import React, { useState } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";

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

  const enableCard = (index) => {
    const cardsElected = cardPool;
    cardsElected[index] = !cardsElected[index];
    if (cardsElected.filter(Boolean).length >= hand.length - 1)
      setCardPool(cardsElected);
    else alert("You cant choose more than " + hand.length - 1 + " cards");
  };

  const sendLegislativeSession = async () => {
    const url = "http://127.0.0.1:8000";
    const discarded = hand.find((card, index) => !cardPool[index]);
    await fetch(
      url + `/game/${game.id}/proclamation/${user.id}?discarded=${discarded}`,
      {
        method: "POST",
        body: hand.filter((card, index) => cardPool[index]),
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

  return (
    <div>
      <button
        onClick={() => {
          setOpen(true);
        }}
      >
        Choose Proclamations
      </button>
      <Modal
        isOpen={open}
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
        <div>
          {hand.map((card, index) => (
            <h4
              onClick={() => {
                enableCard(index);
              }}
              className={cardPool[index] ? "Selected" : "NotSelected"}
            >
              {card}
            </h4>
          ))}
          {cardPool.filter(Boolean).length === hand.length - 1 ? (
            <h2
              onClick={() => {
                sendLegislativeSession();
              }}
            >
              Send Cards
            </h2>
          ) : (
            ""
          )}
        </div>
      </Modal>
    </div>
  );
}

export default LegislativeSession;
