import loginReducer from "./login";
import registerReducer from "./register";
import { combineReducers } from "redux";

const reducers = combineReducers({
  logged_in: loginReducer,
  register: registerReducer
});

export default reducers;
