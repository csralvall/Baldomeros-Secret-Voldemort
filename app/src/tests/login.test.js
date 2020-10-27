import React from "react";
import { Provider } from 'react-redux';
import Enzyme, { shallow, mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import { Link } from 'react-router';
import Login from "../components/Login";
import reducers from "../reducers/index";


Enzyme.configure({ adapter: new Adapter() });

describe("Login Interface", () => {
  

  const store = createStore(reducers);
  const wrapper = mount(
    <Provider store={store}>
      <Login/>
    </Provider>
  );

  it("should show Login title", () => {
    const title = wrapper.find("div h1");
    expect(title.text()).toBe("Enter User Info");
  });
  it("should show Login form", () => {
    const form = wrapper.find("div form");
    expect(form.exists()).toBe(true);
  });
  it("should show Login form inputs", () => {
    const inputs = wrapper.find("div form input");
    expect(inputs).toHaveLength(2);
  });
  it("should show Login form labels", () => {
    const labels = wrapper.find("div form label");
    expect(labels).toHaveLength(2);
  });
  it("should show Login form labels' text", () => {
    const labels = wrapper.find("div form label");
    expect(labels.at(0).text()).toBe("Username");
    expect(labels.at(1).text()).toBe("Password");
  });
  it("should show Login button", () => {
    const button = wrapper.find("div form button");
    expect(button.exists()).toBe(true);
  });
  it("should show Login button's text", () => {
    const button = wrapper.find("div form button");
    expect(button.text()).toBe("Login");
  });
  it("all fields are required", () => {
    const inputs = wrapper.find("div form input");
    expect(inputs.everyWhere((n) => n.prop("required"))).toBe(true);
  });
  it("Password field required password", () => {
    const inputs = wrapper.find("div form input");
    const passwordInput = inputs.findWhere(
      (n) => n.prop("type") === "password"
    );
    expect(passwordInput.exists()).toBe(true);
  });
  //DATA INPUTS
  it("Username input must update", () => {  
    const userInput = wrapper.find('div form input').findWhere(
      (n) => n.prop("type") === "username") 
    userInput.simulate('change', { target: { value: 'avc' } })
    // Manual re-render. "update" method doesn't work;
    //this appears to be the only way
    const Input = wrapper.find('div form input').findWhere(
      (n) => n.prop("type") === "username")
    expect(Input.prop("value")).toBe('avc')
  })
  it("Password input must update",() => {
    const passwordInput = wrapper.find('div form input').findWhere(
    (n) => n.prop("type") === "password");
    passwordInput.simulate('change', { target: { value: "123" } });
    //Manual re-render. "update" method doesn't work;
    //this appears to be the only way
    const Input = wrapper.find('div form input').findWhere(
      (n) => n.prop("type") === "password")
    expect(Input.prop("value")).toBe('123')
  })
});