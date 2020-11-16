import React, { useState } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import "./css/Nomination.css";

if (process.env.NODE_ENV === "test") {
  Modal.setAppElement("*");
} else {
  Modal.setAppElement("#root");
}

function Nomination() {
  const matchID = useSelector((state) => state.match.id);
  const [candidates, setCandidates] = useState([]);
  const [open, setOpen] = useState(false);

  const getCandidates = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/game/${matchID}/directors`, {
      method: "GET",
    })
      .then(async (response) => {
        const responseData = await response.json();
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Match doesn't exist");
          } else {
            alert("Unknown Error.");
          }
        } else {
          setCandidates(responseData["posible directors"]);
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  const sendCandidate = async (candidate) => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/game/${matchID}/director?playername=${candidate}`, {
      method: "PATCH",
    })
      .then((response) => {
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Failed to send candidate. Try again");
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
          getCandidates();
          setOpen(true);
        }}
        className="nomination-btn"
      >
        Nominate Director
      </button>
      <Modal
        isOpen={open}
        closeTimeoutMS={200}
        onRequestClose={() => {
          setOpen(false);
        }}
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
          <h1 className="nomination-modal-title">Nominate Director</h1>
          {candidates.map((player) => (
            <h4
              onClick={() => {
                sendCandidate(player);
              }}
              className="player-name-nomination"
            >
              {player}
            </h4>
          ))}
        </div>
      </Modal>
    </div>
  );
}

export default Nomination;
