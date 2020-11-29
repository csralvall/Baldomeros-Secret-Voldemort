import React from "react";
import ChangePassword from "./ChangePassword";
import ChangeEmail from "./ChangeEmail";

function Profile() {
  return (
    <div className="sign-up-module">
      <h1 className="sign-up-title">My Profile</h1>
      <ChangePassword />
      <ChangeEmail />
    </div>
  );
}

export default Profile;
