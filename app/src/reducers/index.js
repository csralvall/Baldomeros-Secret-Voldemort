import loginReducer from "./login";
import { combineReducers } from "redux";

const reducers = combineReducers({
  logged_in: loginReducer,
});

export default reducers;
