import React from "react";
import ProfileInfo from "./ProfileInfo";
import ChangePassword from "./ChangePassword";
import ChangeEmail from "./ChangeEmail";

function Profile() {
  return (
    <div className="profile-module">
      <h1 className="profile-title">My Profile</h1>
      <hr className="line" />
      <ProfileInfo />
      <hr className="line" />
      <h1 className="change-info-title">Change Info</h1>
      <ChangePassword />
      <ChangeEmail />
    </div>
  );
}

export default Profile;
