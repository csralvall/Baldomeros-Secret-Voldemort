import React from "react";
import { Provider } from "react-redux";
import Enzyme, { mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import CreateMatch from "../components/CreateMatch";
import reducers from "../reducers/index";

Enzyme.configure({ adapter: new Adapter() });

describe("Create Match if Logged In", () => {
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
      <CreateMatch />
    </Provider>
  );

  it("should show Create Match title", () => {
    const title = wrapper.find("div h1").at(0);
    expect(title.text()).toBe("Create Match");
  });
  it("should show minPlayers", () => {
    const title = wrapper.find("div h1").at(1);
    expect(title.text()).toBe("5");
  });
  it("should show maxPlayers", () => {
    const title = wrapper.find("div h1").at(2);
    expect(title.text()).toBe("10");
  });
  it("should show Create Match form", () => {
    const form = wrapper.find("div form");
    expect(form.exists()).toBe(true);
  });
  it("should show Slider", () => {
    expect(wrapper.find("div Slider").exists()).toBe(true);
  });
  it("should show Create Match form labels", () => {
    const labels = wrapper.find("div form label");
    expect(labels).toHaveLength(2);
  });
  it("should show Create Match form labels' text", () => {
    const labels = wrapper.find("div form label");
    expect(labels.at(0).text()).toBe("Min Players5");
    expect(labels.at(1).text()).toBe("Max Players10");
  });
  it("should show Create Match button", () => {
    const button = wrapper.find("div form button");
    expect(button.exists()).toBe(true);
  });
  it("should show Create Match button's text", () => {
    const button = wrapper.find("div form button");
    expect(button.text()).toBe("Play");
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
      <CreateMatch />
    </Provider>
  );

  it("should only show one h1", () => {
    expect(wrapper).toHaveLength(1);
    const title = wrapper.find("div h1");
    expect(title).toHaveLength(1);
  });
  it("should have correct text", () => {
    const title = wrapper.find("div h1");
    expect(title.text()).toBe("Please Log In to create match");
  });
});
