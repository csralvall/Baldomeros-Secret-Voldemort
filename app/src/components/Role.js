import React, { useEffect, useState, useRef } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import harry2 from "../media/roles/harry2.png";
import ron from "../media/roles/ron.png";
import hermione from "../media/roles/hermione.png";
import sirius from "../media/roles/sirius.png";
import dumbledore from "../media/roles/dumbledore.png";
import weasley1 from "../media/roles/weasley1.png";
import weasley2 from "../media/roles/weasley2.png";
import bellatrix from "../media/roles/bellatrix.png";
import umbridge from "../media/roles/umbridge.png";
import malfoyPadre from "../media/roles/malfoyPadre.png";
import draco from "../media/roles/draco.png";
import voldemort from "../media/roles/voldemort.png";
import snapeDeathEater from "../media/roles/snapeDeathEater.png";

import "./css/Role.css";

if (process.env.NODE_ENV === "test") {
  Modal.setAppElement("*");
} else {
  Modal.setAppElement("#root");
}

function Role() {
  const matchID = useSelector((state) => state.match.id);
  const playerID = useSelector((state) => state.match.playerId);
  const [role, setRole] = useState("");
  const [roleImg, setRoleImg] = useState();
  const [open, setOpen] = useState(false);
  const [isFirstTime, setIsFirstTime] = useState(true);

  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      getRole();
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isFirstTime]);

  const getRole = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/game/${matchID}/player/${playerID}/rol`, {
      method: "GET",
    })
      .then(async (response) => {
        const responseData = await response.json();
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Match or player don't exist");
          } else {
            alert("Could not get Role. Unknown Error.");
          }
        } else {
          setRole(responseData.rol);
          setRoleImg(getRoleImg(responseData.rol));
          console.log(responseData.rol);
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  const getRoleImg = (role) => {
    if (role === "Death Eater") {
      const deathEatersImgArray = [
        draco,
        malfoyPadre,
        umbridge,
        bellatrix,
        snapeDeathEater,
      ];
      const randomIndex = Math.floor(
        Math.random() * deathEatersImgArray.length
      );
      return deathEatersImgArray[randomIndex];
    } else if (role === "Order of the Phoenix") {
      const orderOfThePhoenixImgArray = [
        harry2,
        ron,
        hermione,
        dumbledore,
        weasley1,
        weasley2,
        sirius,
      ];
      const randomIndex = Math.floor(
        Math.random() * orderOfThePhoenixImgArray.length
      );
      return orderOfThePhoenixImgArray[randomIndex];
    } else {
      return voldemort;
    }
  };

  return (
    <div>
      <button
        onClick={() => {
          setOpen(true);
          setIsFirstTime(false);
        }}
      >
        Secret Role
      </button>
      <Modal
        isOpen={open}
        closeTimeoutMS={200}
        onRequestClose={() => setOpen(false)}
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
          <img src={roleImg} className="role-img" alt="logo" />
        </div>
      </Modal>
    </div>
  );
}

export default Role;

