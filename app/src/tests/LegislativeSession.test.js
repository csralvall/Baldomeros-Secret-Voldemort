import React from "react";
import { Provider } from "react-redux";
import Enzyme, { mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import reducers from "../reducers/index";
import LegislativeSession from "../components/LegislativeSession";

Enzyme.configure({ adapter: new Adapter() });

describe("Legislative Session", () => {
  const store = createStore(reducers, {});
  function wrap() {
    return mount(
      <Provider store={store}>
        <LegislativeSession hand={["nox", "lumos", "nox"]} />
      </Provider>
    );
  }

  it("should show Modal", () => {
    const wrapper = wrap();
    const modal = wrapper.find("div Modal");
    expect(modal.exists()).toBe(true);
  });
  it("shouldn't show cards if modal is closed", () => {
    const wrapper = wrap();
    const cards = wrapper.find("div Modal div h4");
    expect(cards).toHaveLength(0);
  });
  it("should show three cards if modal opens", () => {
    const wrapper = wrap();
    const button = wrapper.find("div button");
    button.simulate("click");
    const cards = wrapper.find("div Modal div h4");
    expect(cards).toHaveLength(3);
  });
  it("should show correct cards if modal opens", () => {
    const wrapper = wrap();
    const button = wrapper.find("div button");
    button.simulate("click");
    const cards = wrapper.find("div Modal div h4");
    expect(cards.at(0).text()).toBe("nox");
    expect(cards.at(1).text()).toBe("lumos");
    expect(cards.at(2).text()).toBe("nox");
  });

  //Further testing is impossible, since wrapper wont re-render
});
