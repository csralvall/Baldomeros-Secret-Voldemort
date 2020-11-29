import React, { useEffect, useState, useRef } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import "./css/AvadaKedavra.css";
import "./css/LegislativeSession.css";
import "./css/Role.css";
import phoenixProclamation from "../media/cards/phoenixProclamation.png";
import deathEaterProclamation from "../media/cards/deathEaterProclamation.png";

if (process.env.NODE_ENV === "test") {
  Modal.setAppElement("*");
} else {
  Modal.setAppElement("#root");
}

function Crucio({ playerList }) {
  const matchID = useSelector((state) => state.match.id);
  const username = useSelector((state) => state.user.username);
  const [victim, setVictim] = useState(0);
  const [victimRole, setVictimRole] = useState("");
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
      castCrucio();
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [victim]);

  const castCrucio = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(
      url +
        `/game/${matchID}/board/crucio?playername=${username}&investigated=${victim}`,
      {
        method: "GET",
      }
    )
      .then(async (response) => {
        const responseData = await response.json();
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Failed to cast the spell. Try again");
          } else {
            alert("Unknown Error.");
          }
        } else {
          setVictimRole(responseData);
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  const endCrucio = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/game/${matchID}/board/no-spell`, {
      method: "PATCH",
    })
      .then((response) => {
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Failed, try again");
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

  const crucioNotCasted = (
    <div>
      <h1 className="avada-kedavra-modal-title">Cast Crucio</h1>
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
  );

  const crucioCasted = (
    <div>
      <h1 className="avada-kedavra-modal-title">{victim} alliegance is with</h1>
      <img
        src={
          victimRole === "Death Eater"
            ? deathEaterProclamation
            : phoenixProclamation
        }
        className="not-selected-proc"
        alt="logo"
      />
      <div className="send-cards-btn-div">
        <button
          className="send-cards-btn"
          onClick={() => {
            endCrucio();
          }}
        >
          Done
        </button>
      </div>
    </div>
  );

  return (
    <div>
      <button
        className="avada-kedavra-btn"
        onClick={() => {
          setOpen(true);
        }}
      >
        Cast Crucio
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
        {victimRole === "" ? crucioNotCasted : crucioCasted}
      </Modal>
    </div>
  );
}

export default Crucio;
