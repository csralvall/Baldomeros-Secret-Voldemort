import loginReducer from "./login";
import matchReducer from "./match";
import { combineReducers } from "redux";

const reducers = combineReducers({
  logged_in: loginReducer,
  match: matchReducer
});

export default reducers;
