import loginReducer from "./login";
import registerReducer from "./register";
import { combineReducers } from "redux";

const reducers = combineReducers({
  user: loginReducer,
  register: registerReducer,
});

export default reducers;
