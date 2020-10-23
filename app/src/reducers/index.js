import loginReducer from "./login";
import registerReducer from "./register";
import matchReducer from "./match";
import { combineReducers } from "redux";

const reducers = combineReducers({
  logged_in: loginReducer,
  register: registerReducer,
  match: matchReducer
});

export default reducers;
