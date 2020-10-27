import { act } from "react-dom/test-utils";
import React from "react";

const loginReducer = (state = {token: 0, logged_in: false, username :"", id:0}, action) => {
  switch (action.type) {
    case "LOGIN":
      if (action.payload.token == 145)
        return {token : action.payload.token,
                logged_in: true,
                username: action.payload.username,
                id: action.payload.id};
      else
        return state;    
    default:
      return state;
  }
};
export default loginReducer;
