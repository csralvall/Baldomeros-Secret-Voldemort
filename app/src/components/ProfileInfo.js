import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import "./css/Profile.css";

function ProfileInfo() {
  const user = useSelector((state) => state.user);
  const [info, setInfo] = useState({});

  useEffect(() => {
    fetchProfileInfo();
  }, []);

  const fetchProfileInfo = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(url + `/game/profile?user_id=${user.id}`, {
      method: "POST",
    })
      .then(async (response) => {
        const responseData = await response.json();
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Didn't find user");
          } else {
            alert("Could not fetch profile info. Unknown Error.");
          }
        } else {
          setInfo(responseData);
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  return (
    <div className="profile-info-module">
      <h1 className="profile-info-title">Profile Info</h1>
      <div className="profile-info-content">
        <div className="profile-info-content-item">
          <h1 className="profile-info-labels">Username</h1>
          <h1 className="username">{info.Username}</h1>
        </div>
        <div className="profile-info-content-item">
          <h1 className="profile-info-labels">E-Mail</h1>
          <h1 className="email">{info.Email}</h1>
        </div>
      </div>
    </div>
  );
}
export default ProfileInfo;
