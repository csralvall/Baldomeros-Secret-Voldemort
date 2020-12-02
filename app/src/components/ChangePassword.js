import React, { useState, useRef, useEffect } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import "./css/Profile.css";

function ChangePassword() {
  const user = useSelector((state) => state.user);
  const [passwordModalOpen, setPasswordModalOpen] = useState(false);
  const [newPassword, setNewPassword] = useState("");
  const [oldPassword, setOldPassword] = useState("");
  const [changePasswordData, setChangePasswordData] = useState({});

  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      changePassword();
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [changePasswordData]);

  const updateOldPassword = (e) => {
    setOldPassword(e.target.value);
  };

  const updateNewPassword = (e) => {
    setNewPassword(e.target.value);
  };

  const getChangePasswordData = (e) => {
    e.preventDefault();
    setChangePasswordData({
      user_id: user.id,
      oldp: oldPassword,
      newp: newPassword,
    });
  };

  const changePassword = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(
      url +
        `/password?user_id=${changePasswordData.user_id}&oldp=${changePasswordData.oldp}&newp=${changePasswordData.newp}`,
      {
        method: "POST",
      }
    )
      .then((response) => {
        console.log(response);
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Invalid Password");
          } else {
            alert("Could not Change Password. Unknown Error.");
          }
        } else {
          alert("Success!");
          setPasswordModalOpen(false);
          setNewPassword("");
          setOldPassword("");
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  return (
    <div className="change-pass-module">
      <button
        className="profile-info-btn"
        onClick={() => {
          setPasswordModalOpen(true);
        }}
      >
        Change Password
      </button>
      <Modal
        isOpen={passwordModalOpen}
        closeTimeoutMS={200}
        onRequestClose={() => {
          setPasswordModalOpen(false);
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
        <div>
          <form onSubmit={getChangePasswordData} className="sign-up-form">
            <label className="profile-labels">
              Old Password
              <input
                className="text-input"
                type="password"
                value={oldPassword}
                onChange={updateOldPassword}
                required
              />
            </label>
            <label id="bottom-label" className="profile-labels">
              New Password
              <input
                className="text-input"
                type="password"
                value={newPassword}
                onChange={updateNewPassword}
                required
              />
            </label>
            <div className="button-sign-up-wrapper">
              <button type="submit" className="button-sign-up">
                Send
              </button>
            </div>
          </form>
        </div>
      </Modal>
    </div>
  );
}
export default ChangePassword;
