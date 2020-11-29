import React, { useState } from "react";
import useInterval from "react-useinterval";
import { useSelector } from "react-redux";
import AvadaKedavra from "./AvadaKedavra";
import Adivination from "./Adivination";
import "./css/Match.css";
import Crucio from "./Crucio";

function Spell({ availableSpell, hand, playerList, minister }) {
  function spellSwitch(spell) {
    switch (spell) {
      case "Adivination":
        return <Adivination hand={hand} />;
      case "Avada Kedavra":
        return <AvadaKedavra playerList={playerList} />;
      case "Crucio":
        return <Crucio playerList={playerList} />;
      default:
        return "";
    }
  }

  return (
    <div>
      <h1>
        Minister {minister} is casting {availableSpell}
      </h1>
      {spellSwitch(availableSpell)}
    </div>
  );
}
export default Spell;
