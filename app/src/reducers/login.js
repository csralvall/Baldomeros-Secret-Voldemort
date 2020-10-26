import { act } from "react-dom/test-utils";

const loginReducer = (state = {token: 0, logged_in: false, username :"", id:0}, action) => {
  switch (action.type) {
    case "LOGIN":
      if (action.payload.token = 145)
        return (action.payload).append("logged_in",true);
      else
        return state;    
    default:
      return state;
  }
};
export default loginReducer;
