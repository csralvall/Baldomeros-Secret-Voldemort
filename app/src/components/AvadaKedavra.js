import React, { useEffect, useState, useRef } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import "./css/AvadaKedavra.css";

if (process.env.NODE_ENV === "test") {
  Modal.setAppElement("*");
} else {
  Modal.setAppElement("#root");
}

function AvadaKedavra({ playerList }) {
  const matchID = useSelector((state) => state.match.id);
  const username = useSelector((state) => state.user.username);
  const [victim, setVictim] = useState(0);
  const [open, setOpen] = useState(false);

  function isPlayerDead(player) {
    return !player[1].isDead;
  }

  function isNotMe(player) {
    return username !== player[0];
  }

  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      castAdavaKedavra();
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [victim]);

  const castAdavaKedavra = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(
      url + `/game/${matchID}/board/avada-kedavra/?playername=${victim}`,
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
        className="avada-kedavra-btn"
        onClick={() => {
          setOpen(true);
        }}
      >
        Cast Avada Kedavra
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
          <h1 className="avada-kedavra-modal-title">Cast Avada Kedavra</h1>
          {Object.entries(playerList)
            .filter(isPlayerDead)
            .filter(isNotMe)
            .map((player) => (
              <h4
                onClick={() => {
                  setVictim(player[0]);
                }}
                className="player-name-avada-kedavra"
              >
                {player[0]}
              </h4>
            ))}
        </div>
      </Modal>
    </div>
  );
}

export default AvadaKedavra;
