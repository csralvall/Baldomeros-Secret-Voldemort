import React, { useEffect, useState, useRef } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import lumos from "../media/Lumos.png";
import nox from "../media/Nox.png";
import "./Vote.css";

if (process.env.NODE_ENV === "test") {
  Modal.setAppElement("*");
} else {
  Modal.setAppElement("#root");
}

function Vote() {
  const matchID = useSelector((state) => state.match.id);
  const playerID = useSelector((state) => state.match.playerId);
  const [currentVote, setCurrentVote] = useState("");
  const [open, setOpen] = useState(false);

  //flag for voting when the vote is the same as the last
  const [voteFlag, setFlag] = useState(false);
  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      sendVote();
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentVote, voteFlag]);

  const sendVote = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(
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
        Vote
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
          <img
            src={lumos}
            onClick={() => {
              setCurrentVote("lumos");
              setFlag(!voteFlag);
            }}
            style={{ cursor: "pointer" }}
            className="nav-logo"
            alt="logo"
          />
          <img
            src={nox}
            onClick={() => {
              setCurrentVote("nox");
              setFlag(!voteFlag);
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
