import React from "react";
import { Provider } from "react-redux";
import Enzyme, { shallow, mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import Election from "../components/Election";
import reducers from "../reducers/index";

Enzyme.configure({ adapter: new Adapter() });

describe("Election Interface", () => {
  const store = createStore(reducers);
  function wrap() {
    return mount(
      <Provider store={store}>
        <Election
          playerList={{
            "Tom Riddle": { vote: "missing vote", isDead: false },
            "Harry Potter": { vote: "Lumos", isDead: false },
            Dumbledore: { vote: "Nox", isDead: false },
            "Severus Snape": { vote: "Missing Vote", isDead: true },
          }}
          minister={"Tom Riddle"}
        />
      </Provider>
    );
  }

  it("should show vote button if you didn't vote", () => {
    store.getState().user = {
      username: "Tom Riddle",
      id: 1,
      token: 145,
      logged_in: true,
    };
    const wrapper = wrap();
    const button = wrapper.find("div div button");
    expect(button.exists()).toBe(true);
  });

  it("shouldn't show button if you already voted", () => {
    store.getState().user = {
      username: "Harry Potter",
      id: 2,
      token: 145,
      logged_in: true,
    };
    const wrapper = wrap();
    const button = wrapper.find("div div button");
    expect(button.exists()).toBe(false);
  });

  it("shouldn't show button if you are dead", () => {
    store.getState().user = {
      username: "Severus Snape",
      id: 3,
      token: 145,
      logged_in: true,
    };
    const wrapper = wrap();
    const button = wrapper.find("div div button");
    expect(button.exists()).toBe(false);
  });

  it("should show minister name", () => {
    const wrapper = wrap();
    const list = wrapper.find("div h1");
    expect(list.text()).toBe("The current minister is Tom Riddle");
  });

  it("should show player list with their correct votes", () => {
    const wrapper = wrap();
    const list = wrapper.find("div h4");
    expect(list).toHaveLength(4);
    expect(list.at(0).text()).toBe("Tom Riddle voted missing vote");
    expect(list.at(1).text()).toBe("Harry Potter voted Lumos");
    expect(list.at(2).text()).toBe("Dumbledore voted Nox");
  });

  it("Shouldn't show dead players in player list", () => {
    const wrapper = wrap();
    const list = wrapper.find("div h4");
    expect(list.at(4).exists()).toBe(false);
  });
});
