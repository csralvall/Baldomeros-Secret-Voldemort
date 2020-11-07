import React from "react";
import { Provider } from "react-redux";
import Enzyme, { mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import Nav from "../components/Nav";
import reducers from "../reducers/index";
import { BrowserRouter } from "react-router-dom";

Enzyme.configure({ adapter: new Adapter() });

describe("Navigation Bar", () => {
  const store = createStore(reducers);
  function wrap() {
    return mount(
      <Provider store={store}>
        <BrowserRouter>
          <Nav />
        </BrowserRouter>
      </Provider>
    );
  }

  it("should show title img", () => {
    const wrapper = wrap();
    const title = wrapper.find("div nav img").at(0);
    expect(title.exists()).toBe(true);
  });

  it("Should show correct options if logged out", () => {
    const wrapper = wrap();
    const links = wrapper.find("div nav ul Link li");
    expect(links.at(0).text()).toBe("Home");
    expect(links.at(1).text()).toBe("Login");
    expect(links.at(2).text()).toBe("Sign Up");
  });

  it("Should show correct options if logged in", () => {
    store.getState().user = {
      token: 145,
      logged_in: true,
      username: "Tom Riddle",
      id: 1,
    };
    const wrapper = wrap();
    const links = wrapper.find("div nav ul Link li");
    expect(links.at(0).text()).toBe("Home");
    expect(links.at(1).text()).toBe("Profile");
    expect(links.at(2).text()).toBe("Log Out");
  });

  it("Should log out on click", () => {
    const wrapper = wrap();
    const logoutLink = wrapper.find("div nav ul Link li").at(2);
    logoutLink.simulate("click");
    expect(store.getState().user.token).toBe(0);
    expect(store.getState().user.id).toBe(0);
    expect(store.getState().user.logged_in).toBe(false);
    expect(store.getState().user.userrname).toBe(undefined);
  });
});
