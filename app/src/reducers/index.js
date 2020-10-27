import loginReducer from "./login";
import { combineReducers } from "redux";

const reducers = combineReducers({
  user: loginReducer,
});

export default reducers;
