import loginReducer from "./login";
import StoreMatchReducer from "./storeMatch";
import { combineReducers } from "redux";

const reducers = combineReducers({
  user: loginReducer,
  match: StoreMatchReducer,
});

export default reducers;
