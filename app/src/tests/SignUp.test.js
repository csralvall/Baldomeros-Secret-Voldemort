import React from "react";
import Enzyme, { shallow } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import SignUp from "../components/SignUp";

Enzyme.configure({ adapter: new Adapter() });

describe("SignUp Interface", () => {
  it("should show Sign Up title", () => {
    const wrapper = shallow(<SignUp />);
    const title = wrapper.find("div h1");
    expect(title.text()).toBe("Sign Up");
  });
  it("should show Sign Up form", () => {
    const wrapper = shallow(<SignUp />);
    const form = wrapper.find("div form");
    expect(form.exists()).toBe(true);
  });
  it("should show Sign Up form inputs", () => {
    const wrapper = shallow(<SignUp />);
    const inputs = wrapper.find("div form input");
    expect(inputs).toHaveLength(3);
  });
  it("should show Sign Up form labels", () => {
    const wrapper = shallow(<SignUp />);
    const labels = wrapper.find("div form label");
    expect(labels).toHaveLength(3);
  });
  it("should show Sign Up form labels' text", () => {
    const wrapper = shallow(<SignUp />);
    const labels = wrapper.find("div form label");
    expect(labels.at(0).text()).toBe("Username");
    expect(labels.at(1).text()).toBe("Password");
    expect(labels.at(2).text()).toBe("E-Mail");
  });
  it("should show Sign Up button", () => {
    const wrapper = shallow(<SignUp />);
    const button = wrapper.find("div form button");
    expect(button.exists()).toBe(true);
  });
  it("should show Sign Up button's text", () => {
    const wrapper = shallow(<SignUp />);
    const button = wrapper.find("div form button");
    expect(button.text()).toBe("Sign Up");
  });
});

describe("SignUp inputs", () => {
  it("all fields are required", () => {
    const wrapper = shallow(<SignUp />);
    const inputs = wrapper.find("div form input");
    expect(inputs.everyWhere((n) => n.prop("required"))).toBe(true);
  });
  it("E-Mail field required email", () => {
    const wrapper = shallow(<SignUp />);
    const inputs = wrapper.find("div form input");
    const emailInput = inputs.findWhere((n) => n.prop("type") === "email");
    expect(emailInput.exists()).toBe(true);
  });
  it("Password field required password", () => {
    const wrapper = shallow(<SignUp />);
    const inputs = wrapper.find("div form input");
    const passwordInput = inputs.findWhere(
      (n) => n.prop("type") === "password"
    );
    expect(passwordInput.exists()).toBe(true);
  });
});
