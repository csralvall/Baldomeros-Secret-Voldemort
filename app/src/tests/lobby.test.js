import React from "react";
import { Provider } from "react-redux";
import Enzyme, { mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import Lobby from "../components/Lobby";
import reducers from "../reducers/index";

Enzyme.configure({ adapter: new Adapter() });

describe("Lobby if Logged In", () => {
  const store = createStore(reducers, {
    user: {
      token: 145,
      logged_in: true,
      username: "guido",
      id: 1,
    },
  });
  const wrapper = mount(
    <Provider store={store}>
      <Lobby />
    </Provider>
  );

  it("should show title img", () => {
    const title = wrapper.find("div img").at(0);
    expect(title.exists()).toBe(true);
  });
  it("should show two buttons", () => {
    const buttons = wrapper.find("div div button");
    expect(buttons).toHaveLength(2);
  });
  it("should show two buttons' text", () => {
    const buttons = wrapper.find("div div button");
    expect(buttons.at(0).text()).toBe("Create Match");
    expect(buttons.at(1).text()).toBe("Join Match");
  });
  it("should show tiles", () => {
    const tiles = wrapper.find("div .img-tiles div");
    expect(tiles).toHaveLength(12);
  });
});

describe("Create Match if Not Logged In", () => {
  const store = createStore(reducers, {
    user: {
      token: 145,
      logged_in: false,
      username: "guido",
      id: 1,
    },
  });
  const wrapper = mount(
    <Provider store={store}>
      <Lobby />
    </Provider>
  );

  it("should show two buttons", () => {
    const buttons = wrapper.find("div div button");
    expect(buttons).toHaveLength(2);
  });
  it("should show two buttons' text", () => {
    const buttons = wrapper.find("div div button");
    expect(buttons.at(0).text()).toBe("Login");
    expect(buttons.at(1).text()).toBe("Sign Up");
  });
  it("should show tiles", () => {
    const tiles = wrapper.find("div .img-tiles div");
    expect(tiles).toHaveLength(12);
  });
});
