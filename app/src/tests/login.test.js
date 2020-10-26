import React from "react";
import Enzyme, { shallow, mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import Login, { registerUser } from "../components/Login";

Enzyme.configure({ adapter: new Adapter() });

describe("Login Interface", () => {
  it("should show Login title", () => {
    const wrapper = shallow(<Login />);
    const title = wrapper.find("div h1");
    expect(title.text()).toBe("Enter User Info");
  });
  it("should show Login form", () => {
    const wrapper = shallow(<Login />);
    const form = wrapper.find("div form");
    expect(form.exists()).toBe(true);
  });
  it("should show Login form inputs", () => {
    const wrapper = shallow(<Login />);
    const inputs = wrapper.find("div form input");
    expect(inputs).toHaveLength(2);
  });
  it("should show Login form labels", () => {
    const wrapper = shallow(<Login />);
    const labels = wrapper.find("div form label");
    expect(labels).toHaveLength(2);
  });
  it("should show Login form labels' text", () => {
    const wrapper = shallow(<Login />);
    const labels = wrapper.find("div form label");
    expect(labels.at(0).text()).toBe("Username");
    expect(labels.at(1).text()).toBe("Password");
  });
  it("should show Login button", () => {
    const wrapper = shallow(<Login />);
    const button = wrapper.find("div form button");
    expect(button.exists()).toBe(true);
  });
  it("should show Login button's text", () => {
    const wrapper = shallow(<Login />);
    const button = wrapper.find("div form button");
    expect(button.text()).toBe("Login");
  });
});

describe("Login inputs", () => {
  it("all fields are required", () => {
    const wrapper = shallow(<Login />);
    const inputs = wrapper.find("div form input");
    expect(inputs.everyWhere((n) => n.prop("required"))).toBe(true);
  });
  it("Password field required password", () => {
    const wrapper = shallow(<Login />);
    const inputs = wrapper.find("div form input");
    const passwordInput = inputs.findWhere(
      (n) => n.prop("type") === "password"
    );
    expect(passwordInput.exists()).toBe(true);
  });
});