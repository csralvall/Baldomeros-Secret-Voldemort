import loginReducer from "./login";
import signUpReducer from "./signUpReducer";
import { combineReducers } from "redux";

const reducers = combineReducers({
  logged_in: loginReducer,
  hasSignedUp: signUpReducer
});

export default reducers;
