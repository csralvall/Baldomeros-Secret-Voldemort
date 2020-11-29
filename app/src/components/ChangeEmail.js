import React, { useState, useRef, useEffect } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import "./css/Profile.css";

function ChangeEmail() {
  const user = useSelector((state) => state.user);
  const [emailModalOpen, setEmailModalOpen] = useState(false);
  const [newEmail, setNewEmail] = useState("");
  const [oldEmail, setOldEmail] = useState("");
  const [changeEmailData, setChangeEmailData] = useState({});

  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      changeEmail();
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [changeEmailData]);

  const updateOldEmail = (e) => {
    setOldEmail(e.target.value);
  };

  const updateNewEmail = (e) => {
    setNewEmail(e.target.value);
  };

  const getChangeEmailData = (e) => {
    e.preventDefault();
    setChangeEmailData({
      user_id: user.id,
      olde: oldEmail,
      newe: newEmail,
    });
  };

  const changeEmail = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(
      url +
        `/email?user_id=${changeEmailData.user_id}&olde=${changeEmailData.olde}&newe=${changeEmailData.newe}`,
      {
        method: "POST",
      }
    )
      .then((response) => {
        console.log(response);
        if (response.status !== 200) {
          if (response.status === 404) {
            alert("Invalid Email");
          } else {
            alert("Could not Change Email. Unknown Error.");
          }
        } else {
          alert("Success!");
          setEmailModalOpen(false);
          setNewEmail("");
          setOldEmail("");
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  return (
    <div className="change-pass-module">
      <button
        className="vote-btn"
        onClick={() => {
          setEmailModalOpen(true);
        }}
      >
        Change Email
      </button>
      <Modal
        isOpen={emailModalOpen}
        closeTimeoutMS={200}
        onRequestClose={() => {
          setEmailModalOpen(false);
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
          <form onSubmit={getChangeEmailData} className="sign-up-form">
            <label className="profile-labels">
              Old Email
              <input
                className="text-input"
                type="email"
                value={oldEmail}
                onChange={updateOldEmail}
                required
              />
            </label>
            <label id="bottom-label" className="profile-labels">
              New Email
              <input
                className="text-input"
                type="email"
                value={newEmail}
                onChange={updateNewEmail}
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
export default ChangeEmail;
