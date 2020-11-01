import React from "react";
import { Provider } from "react-redux";
import Enzyme, { mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import Vote from "../components/Vote";
import reducers from "../reducers/index";

Enzyme.configure({ adapter: new Adapter() });

describe("Vote if open", () => {
  const store = createStore(reducers, {});
  const wrapper = mount(
    <Provider store={store}>
      <Vote open={true} />
    </Provider>
  );

  it("should show Modal", () => {
    const modal = wrapper.find("div Modal");
    expect(modal.exists()).toBe(true);
  });
  it("should show two img", () => {
    const imgs = wrapper.find("div Modal div img");
    expect(imgs).toHaveLength(2);
  });
});

describe("Vote if not open", () => {
  const store = createStore(reducers, {});
  const wrapper = mount(
    <Provider store={store}>
      <Vote open={false} />
    </Provider>
  );

  it("should show Modal", () => {
    const modal = wrapper.find("div Modal");
    expect(modal.exists()).toBe(true);
  });
  it("should show empty Modal", () => {
    const imgs = wrapper.find("div Modal div img");
    expect(imgs).toHaveLength(0);
  });
});
