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

function Lobby() {
  const user = useSelector((state) => state.user);
  const history = useHistory();

  return (
    <div>
      <img src={logo} className="logo" />
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
            <button
              className="join-match-btn"
              onClick={() => {
                history.push("/match/join");
              }}
            >
              Join Match
            </button>
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
          <img src={harry2} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={ron} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={hermione} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={malfoyPadre} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={dumbledore} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={weasley1} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={umbridge} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={sirius} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={weasley2} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={draco} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={snapePhoenix} />
          <img className="transition-image" src={voldermort} />
        </div>
        <div className="image-container">
          <img src={bellatrix} />
          <img className="transition-image" src={voldermort} />
        </div>
      </div>
    </div>
  );
}

export default Lobby;
