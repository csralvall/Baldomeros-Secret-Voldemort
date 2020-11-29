import React, { useState, useRef, useEffect } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import "./css/Chat.css";

function Chat() {
  const user = useSelector((state) => state.user);
  const [chatModalOpen, setChatModalOpen] = useState(false);
  const [newMessage, setNewMessage] = useState("");
  const [newMessageData, setNewMessageData] = useState({});

  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      sendMessage();
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [newMessageData]);

  const updateNewMessage = (e) => {
    setNewMessage(e.target.value);
  };

  const getNewMessageData = (e) => {
    e.preventDefault();
    setNewMessageData({
      user_id: user.id,
      msg: newMessage,
    });
  };

  const sendMessage = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(
      url +
        `/password?user_id=${newMessageData.user_id}&oldp=${newMessageData.text}`,
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
          console.log("Success!");
        }
      })
      .catch(() => {
        alert("Network Error");
      });
  };

  return (
    <div className="chat-module">
      <button
        className="chat-btn"
        onClick={() => {
          setChatModalOpen(true);
        }}
      >
        Chat
      </button>
      <Modal
        isOpen={chatModalOpen}
        closeTimeoutMS={200}
        onRequestClose={() => {
          setChatModalOpen(false);
        }}
        className="chat-modal"
      >
        <div>
          <form onSubmit={getNewMessageData} className="send-msg-form">
            <input
              className="chat-msg-input"
              type="text"
              value={newMessage}
              onChange={updateNewMessage}
              required
            />
            <button type="submit" className="button-send-msg">
              Send
            </button>
          </form>
        </div>
      </Modal>
    </div>
  );
}
export default Chat;
