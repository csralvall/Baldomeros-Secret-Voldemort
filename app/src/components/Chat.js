import React, { useState, useRef, useEffect } from "react";
import { useSelector } from "react-redux";
import Modal from "react-modal";
import "./css/Chat.css";

function Chat({ messages }) {
  const user = useSelector((state) => state.user);
  const matchId = useSelector((state) => state.match.id);

  const messagesEndRef = useRef(null);
  const [chatModalOpen, setChatModalOpen] = useState(false);
  const [newMessage, setNewMessage] = useState("");
  const [newMessageData, setNewMessageData] = useState({});
  const [messageCount, setMessageCount] = useState(0);

  const scrollToBottom = () => {
    if (messagesEndRef.current != null) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  const loaded = useRef(false);
  useEffect(() => {
    if (loaded.current) {
      sendMessage();
    } else {
      loaded.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [newMessageData]);

  const loaded2 = useRef(false);

  useEffect(() => {
    if (loaded2.current) {
      scrollToBottom();
    } else {
      loaded2.current = true;
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [messageCount]);

  useEffect(() => {
    if (Object.keys(messages).length !== messageCount) {
      setMessageCount(Object.keys(messages).length);
    }
  }, [messages]);

  const updateNewMessage = (e) => {
    setNewMessage(e.target.value);
  };

  const getNewMessageData = (e) => {
    e.preventDefault();
    setNewMessageData({
      username: user.username,
      msg: newMessage,
    });
  };

  const sendMessage = async () => {
    const url = "http://127.0.0.1:8000";

    await fetch(
      url + `/game/${matchId}/chat?username=${newMessageData.username}`,
      {
        method: "PATCH",
        body: JSON.stringify(newMessageData.msg),
      }
    )
      .then((response) => {
        if (response.status !== 200) {
          if (response.status === 404) {
            alert(
              "You can't send a message if you are dead or selecting proclamations"
            );
          } else {
            alert("Could not Send Message. Unknown Error.");
          }
        } else {
          setNewMessage("");
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
        <div className="chat-div">
          <div className="msg-feed">
            {Object.keys(messages).map((msg) =>
              messages[msg]["Username"] === user.username ? (
                <div className="my-msg-div">
                  <p className="my-msg-p">{messages[msg]["Text"]}</p>
                </div>
              ) : (
                <div className="msg-div">
                  <p className="msg-label">{messages[msg]["Username"]}</p>
                  <p className="msg-p">{messages[msg]["Text"]}</p>
                </div>
              )
            )}
            <div ref={messagesEndRef} />
          </div>
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
