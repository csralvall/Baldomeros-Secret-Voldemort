import React, { useEffect, useState, useRef } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import lumos from "../media/Lumos.png";
import nox from "../media/Nox.png";
import "./Vote.css";

Modal.setAppElement("#root");

function Vote({ open, closeVote }) {
  const matchID = useSelector((state) => state.match.id);
  const playerID = useSelector((state) => state.match.playerId);
  const [currentVote, setCurrentVote] = useState("");

  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      sendVote();
    } else {
      loaded.current = true;
    }
  }, [currentVote]);

  const sendVote = async () => {
    const url = "http://127.0.0.1:8000";

    const response = await fetch(
      url + `/game/${matchID}/player/${playerID}?vote=${currentVote}`,
      {
        method: "PUT",
      }
    )
      .then((response) => {
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Match or player don't exist");
          } else {
            alert("Could not Vote. Unknown Error.");
          }
        } else {
          closeVote();
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  return (
    <div>
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
          <img
            src={lumos}
            onClick={() => {
              setCurrentVote("lumos");
            }}
            style={{ cursor: "pointer" }}
            className="nav-logo"
            alt="logo"
          />
          <img
            src={nox}
            onClick={() => {
              setCurrentVote("nox");
            }}
            style={{ cursor: "pointer" }}
            className="nav-logo"
            alt="logo"
          />
        </div>
      </Modal>
    </div>
  );
}

export default Vote;