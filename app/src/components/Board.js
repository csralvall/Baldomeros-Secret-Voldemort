import React, { useEffect, useState, useRef } from "react";
import phoenixBoard from "../media/boards/phoenixBoard.png";
import phoenixProclamation from "../media/cards/phoenixProclamation.png";
import deathEaterBoard5_6 from "../media/boards/deathEaterBoard5-6.png";
import deathEaterBoard7_8 from "../media/boards/deathEaterBoard7-8.png";
import deathEaterBoard9_10 from "../media/boards/deathEaterBoard9-10.png";
import deathEaterProclamation from "../media/cards/deathEaterProclamation.png";
import chaosCircle from "../media/boards/chaosCircle.png";
import "./css/Board.css";

function Board({
  phoenixProclamationCount,
  deathEaterProclamationCount,
  boardType,
  chaosCirclePosition,
}) {
  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      if (phoenixProclamationCount <= 5 && deathEaterProclamationCount <= 6) {
        updateOpacityArrays(
          phoenixProclamationCount,
          deathEaterProclamationCount
        );
      } else {
        alert(
          "There are more than 5 phoenix or 6 death eater proclamations enacted!"
        );
      }
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phoenixProclamationCount, deathEaterProclamationCount]);

  const updateOpacityArrays = (
    phoenixProclamationCount,
    deathEaterProclamationCount
  ) => {
    var newPhoenixOpacityArray = phoenixOpacityArray;
    for (let i = 0; i < phoenixProclamationCount; i++) {
      newPhoenixOpacityArray[i] = 1;
    }
    setPhoenixOpacityArray(newPhoenixOpacityArray);
    var newDeathEaterOpacityArray = deathEaterOpacityArray;
    for (let i = 0; i < deathEaterProclamationCount; i++) {
      newDeathEaterOpacityArray[i] = 1;
    }
    setDeathEaterOpacityArray(newDeathEaterOpacityArray);
  };
  const [phoenixOpacityArray, setPhoenixOpacityArray] = useState([
    0,
    0,
    0,
    0,
    0,
  ]);
  const [deathEaterOpacityArray, setDeathEaterOpacityArray] = useState([
    0,
    0,
    0,
    0,
    0,
    0,
  ]);

  const getChaosCircleX = (i) => {
    if (i === 0) {
      return "22.5vw";
    } else if (i === 1) {
      return "28.4vw";
    } else if (i === 2) {
      return "34.3vw";
    } else if (i === 3) {
      return "40.2vw";
    }
  };

  const getBoardImg = (type) => {
    if (type === "7-8") {
      return deathEaterBoard7_8;
    } else if (type === "9-10") {
      return deathEaterBoard9_10;
    } else {
      return deathEaterBoard5_6;
    }
  };

  return (
    <div className="boards">
      <div className="phoenix-board-container">
        <img className="phoenix-board-img" src={phoenixBoard} alt=""></img>
        <img
          className="phoenix-proclamation"
          id="phoenix-proclamation-0"
          src={phoenixProclamation}
          alt=""
          style={{ opacity: phoenixOpacityArray[0] }}
        ></img>
        <img
          className="phoenix-proclamation"
          id="phoenix-proclamation-1"
          src={phoenixProclamation}
          alt=""
          style={{ opacity: phoenixOpacityArray[1] }}
        ></img>
        <img
          className="phoenix-proclamation"
          id="phoenix-proclamation-2"
          src={phoenixProclamation}
          alt=""
          style={{ opacity: phoenixOpacityArray[2] }}
        ></img>
        <img
          className="phoenix-proclamation"
          id="phoenix-proclamation-3"
          src={phoenixProclamation}
          alt=""
          style={{ opacity: phoenixOpacityArray[3] }}
        ></img>
        <img
          className="phoenix-proclamation"
          id="phoenix-proclamation-4"
          src={phoenixProclamation}
          alt=""
          style={{ opacity: phoenixOpacityArray[4] }}
        ></img>
      </div>
      <div className="death-eater-board-container">
        <img
          className="death-eater-board-img"
          src={getBoardImg(boardType)}
          alt=""
        ></img>
        <img
          className="death-eater-proclamation"
          id="death-eater-proclamation-0"
          src={deathEaterProclamation}
          alt=""
          style={{ opacity: deathEaterOpacityArray[0] }}
        ></img>
        <img
          className="death-eater-proclamation"
          id="death-eater-proclamation-1"
          src={deathEaterProclamation}
          alt=""
          style={{ opacity: deathEaterOpacityArray[1] }}
        ></img>
        <img
          className="death-eater-proclamation"
          id="death-eater-proclamation-2"
          src={deathEaterProclamation}
          alt=""
          style={{ opacity: deathEaterOpacityArray[2] }}
        ></img>
        <span className="smaller-proclamations">
          <img
            className="death-eater-proclamation"
            id="death-eater-proclamation-3"
            src={deathEaterProclamation}
            alt=""
            style={{ opacity: deathEaterOpacityArray[3] }}
          ></img>
          <img
            className="death-eater-proclamation"
            id="death-eater-proclamation-4"
            src={deathEaterProclamation}
            alt=""
            style={{ opacity: deathEaterOpacityArray[4] }}
          ></img>
          <img
            className="death-eater-proclamation"
            id="death-eater-proclamation-5"
            src={deathEaterProclamation}
            alt=""
            style={{ opacity: deathEaterOpacityArray[5] }}
          ></img>
        </span>
      </div>
      <img
        src={chaosCircle}
        style={{ left: getChaosCircleX(chaosCirclePosition) }}
        className="chaosCircle"
      />
    </div>
  );
}

export default Board;
