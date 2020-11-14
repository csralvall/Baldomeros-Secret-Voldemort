import React from "react";
import { Provider } from "react-redux";
import Enzyme, { mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import reducers from "../reducers/index";
import AvadaKedavra from "../components/AvadaKedavra";

Enzyme.configure({ adapter: new Adapter() });

describe("Cast Avada Kedavra", () => {
  const store = createStore(reducers, {});
  const wrapper = mount(
    <Provider store={store}>
      <AvadaKedavra
        playerList={{
          "Tom Riddle": { vote: "x", isDead: false },
          "Harry Potter": { vote: "x", isDead: false },
          Dumbledore: { vote: "x", isDead: true },
        }}
      />
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
  it("should show two names if modal opens", () => {
    const button = wrapper.find("div button");
    button.simulate("click");
    const list = wrapper.find("div Modal div h4");
    expect(list).toHaveLength(2);
    expect(list.at(0).text()).toBe("Tom Riddle");
    expect(list.at(1).text()).toBe("Harry Potter");
  });
});
