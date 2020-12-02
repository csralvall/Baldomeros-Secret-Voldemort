import React from "react";
import { useSelector } from "react-redux";
import AvadaKedavra from "./AvadaKedavra";
import Adivination from "./Adivination";
import "./css/Match.css";
import Crucio from "./Crucio";
import Imperio from "./Imperio";

function Spell({ availableSpell, hand, playerList, minister }) {
  const username = useSelector((state) => state.user.username);

  function spellSwitch(spell) {
    switch (spell) {
      case "Adivination":
        return <Adivination hand={hand} />;
      case "Avada Kedavra":
        return <AvadaKedavra playerList={playerList} />;
      case "Crucio":
        return <Crucio playerList={playerList} />;
      case "Imperio":
        return <Imperio playerList={playerList} />;
      default:
        return "";
    }
  }

  return (
    <div>
      <h1>
        Minister {minister} is casting {availableSpell}
      </h1>
      {minister === username ? spellSwitch(availableSpell) : ""}
    </div>
  );
}
export default Spell;
