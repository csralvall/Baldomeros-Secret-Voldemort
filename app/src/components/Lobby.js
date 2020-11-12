import React from "react";
import { useHistory } from "react-router-dom";
import { useSelector } from "react-redux";
import harry2 from "../media/roles/harry2.png";
import ron from "../media/roles/ron.png";
import hermione from "../media/roles/hermione.png";
import sirius from "../media/roles/sirius.png";
import dumbledore from "../media/roles/dumbledore.png";
import weasley1 from "../media/roles/weasley1.png";
import weasley2 from "../media/roles/weasley2.png";
import snapePhoenix from "../media/roles/snapePhoenix.png";
import bellatrix from "../media/roles/bellatrix.png";
import umbridge from "../media/roles/umbridge.png";
import malfoyPadre from "../media/roles/malfoyPadre.png";
import draco from "../media/roles/draco.png";
import voldermort from "../media/roles/voldemort.png";
import logo from "../media/logos/logo.png";
import "./css/Lobby.css";
import JoinMatch from "./JoinMatch.js";

function Lobby() {
  const user = useSelector((state) => state.user);
  const history = useHistory();

  return (
    <div>
      <img src={logo} className="logo" alt="" />
      <div className="btns">
        {user.logged_in ? (
          <div>
            <button
              className="create-match-btn"
              onClick={() => {
                history.push("/match/create");
              }}
            >
              Create Match
            </button>
            <JoinMatch className="btns" />
          </div>
        ) : (
          <div>
            <button
              className="login-btn"
              onClick={() => {
                history.push("/login");
              }}
            >
              Login
            </button>
            <button
              className="sign-up-btn"
              onClick={() => {
                history.push("/signup");
              }}
            >
              Sign Up
            </button>
          </div>
        )}
      </div>
      <div className="img-tiles">
        <div className="image-container">
          <img src={harry2} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={ron} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={hermione} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={malfoyPadre} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={dumbledore} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={weasley1} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={umbridge} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={sirius} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={weasley2} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={draco} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={snapePhoenix} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
        <div className="image-container">
          <img src={bellatrix} alt="" />
          <img className="transition-image" src={voldermort} alt="" />
        </div>
      </div>
    </div>
  );
}

export default Lobby;
