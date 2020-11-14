import React from "react";
import { Provider } from "react-redux";
import Enzyme, { mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import reducers from "../reducers/index";
import Nomination from "../components/Nomination";

Enzyme.configure({ adapter: new Adapter() });

describe("Cast Avada Kedavra", () => {
  const store = createStore(reducers, {});
  const wrapper = mount(
    <Provider store={store}>
      <Nomination />
    </Provider>
  );

  it("should show Modal", () => {
    const modal = wrapper.find("div Modal");
    expect(modal.exists()).toBe(true);
  });
  it("shouldn't show list if modal is closed", () => {
    const list = wrapper.find("div Modal div h4");
    expect(list).toHaveLength(0);
  });
  it("should show list if modal opens", () => {
    const button = wrapper.find("div button");
    button.simulate("click");
    const list = wrapper.find("div Modal div");
    expect(list.exists()).toBe(true);
  });
});
