import React from "react";
import { Provider } from "react-redux";
import Enzyme, { shallow, mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import MatchInfo from "../components/MatchInfo";
import reducers from "../reducers/index";

Enzyme.configure({ adapter: new Adapter() });

describe("Match Info Interface", () => {
  const store = createStore(reducers);
  function wrap() {
    return mount(
      <Provider store={store}>
        <MatchInfo
          playerList={{
            "Tom Riddle": { vote: "x", isDead: false },
            "Harry Potter": { vote: "x", isDead: false },
            Dumbledore: { vote: "x", isDead: true },
          }}
        />
      </Provider>
    );
  }

  it("should show if you are the host", () => {
    store.getState().match = { name: "Tom Riddle's Game", id: 2, hostId: 1 };
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

  it("should show start game button if you are the host", () => {
    store.getState().match = { name: "Tom Riddle's Game", id: 2, hostId: 1 };
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

  it("should show if you are not the host", () => {
    store.getState().match = { name: "Tom Riddle's Game", id: 2, hostid: 1 };
    store.getState().user = {
      username: "Harry Potter",
      id: 2,
      token: 145,
      logged_in: true,
    };
    const wrapper = wrap();
    const title = wrapper.find("div h3");
    expect(title.text()).toBe("Waiting for Host to start the game");
  });

  it("shouldn't show button if you are not the host", () => {
    store.getState().match = { name: "Tom Riddle's Game", id: 2, hostid: 1 };
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

  it("should show player list title", () => {
    const wrapper = wrap();
    const list = wrapper.find("div h1");
    expect(list.text()).toBe("Players joined");
  });

  it("should show player list", () => {
    const wrapper = wrap();
    const list = wrapper.find("div h4");
    expect(list).toHaveLength(3);
    expect(list.at(0).text()).toBe("Tom Riddle");
    expect(list.at(1).text()).toBe("Harry Potter");
    expect(list.at(2).text()).toBe("Dumbledore");
  });
});
