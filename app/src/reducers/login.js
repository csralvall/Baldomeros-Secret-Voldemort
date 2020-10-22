import { act } from "react-dom/test-utils";

const loginReducer = (state = {logged_in : false, username :"", id:0}, action) => {
  switch (action.type) {
    case "LOGIN":
      if (action.payload.logged_in)
        return action.payload;
      else
        return state;    
    default:
      return state;
  }
};
export default loginReducer;
