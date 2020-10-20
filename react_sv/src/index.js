import React from "react";
import ReactDOM from "react-dom";
import { createStore } from "redux";
import App from "./App";
import reducers from "./reducers/index";
import { Provider } from "react-redux";

const store = createStore(reducers);
const rootElement = document.getElementById("root");
ReactDOM.render(
  <React.StrictMode>
    <Provider store={store}>
      <App />
    </Provider>
  </React.StrictMode>,
  rootElement
);
