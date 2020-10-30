import loginReducer from "./login";
import matchReducer from "./match";
import { combineReducers } from "redux";

const reducers = combineReducers({
  user: loginReducer,
  match: matchReducer
});

export default reducers;
