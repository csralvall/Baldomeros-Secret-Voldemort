import React from "react";
import { Provider } from "react-redux";
import Enzyme, { shallow, mount } from "enzyme";
import Adapter from "@wojtekmaj/enzyme-adapter-react-17";
import { createStore } from "redux";
import Election from "../components/Election";
import reducers from "../reducers/index";

Enzyme.configure({ adapter: new Adapter() });

describe("Voting Phase Interface", () => {
  const store = createStore(reducers);
  function wrap() {
    return mount(
      <Provider store={store}>
        <Election
          playerList={{
            "Tom Riddle": { vote: "missing vote", isDead: false },
            "Harry Potter": { vote: "Lumos", isDead: false },
            Dumbledore: { vote: "Nox", isDead: false },
            "Severus Snape": { vote: "missing Vote", isDead: true },
          }}
          minister={"Tom Riddle"}
          director={"Dumbledore"}
          status={"election"}
          candidate={"Dumbledore"}
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

  it("should show minister and director names", () => {
    const wrapper = wrap();
    const list = wrapper.find("div div h1");
    expect(list.text()).toBe(
      "Minister Tom Riddle nominated Dumbledore to be Director"
    );
  });

  it("should show player list and if they voted", () => {
    const wrapper = wrap();
    const list = wrapper.find("div h4");
    expect(list).toHaveLength(3);
    expect(list.at(0).text()).toBe("Tom Riddle is voting");
    expect(list.at(1).text()).toBe("Harry Potter voted");
    expect(list.at(2).text()).toBe("Dumbledore voted");
  });

  it("Shouldn't show dead players in player list", () => {
    const wrapper = wrap();
    const list = wrapper.find("div h4");
    expect(list.at(4).exists()).toBe(false);
  });
});

describe("Legislative Session Interface", () => {
  const store = createStore(reducers);
  function wrap() {
    return mount(
      <Provider store={store}>
        <Election
          playerList={{
            "Tom Riddle": { vote: "Lumos", isDead: false },
            "Harry Potter": { vote: "Lumos", isDead: false },
            Dumbledore: { vote: "Nox", isDead: false },
            "Severus Snape": { vote: "missing Vote", isDead: true },
          }}
          minister={"Tom Riddle"}
          director={"Dumbledore"}
          candidate={"Dumbledore"}
          status={"minister selection"}
          hand={["nox", "lumos", "nox"]}
        />
      </Provider>
    );
  }
  store.getState().user = {
    username: "Tom Riddle",
    id: 1,
    token: 145,
    logged_in: true,
  };

  it("should show who's choosing proclamations", () => {
    const wrapper = wrap();
    const list = wrapper.find("div div h1");
    expect(list.text()).toBe("Minister Tom Riddle is choosing proclamations");
  });

  it("shouldt show proclamation button if you have to choose proclamations", () => {
    const wrapper = wrap();
    const button = wrapper.find("div div button");
    expect(button.exists()).toBe(true);
  });

  it("shouldn't show proclamation button if you don't have to choose proclamations", () => {
    store.getState().user = {
      username: "Dumbledore",
      id: 3,
      token: 145,
      logged_in: true,
    };
    const wrapper = wrap();
    const button = wrapper.find("div div button");
    expect(button.exists()).toBe(false);
  });

  it("should show player list and their votes", () => {
    const wrapper = wrap();
    const list = wrapper.find("div h4");
    expect(list).toHaveLength(4);
    expect(list.at(0).text()).toBe("Tom Riddle voted Lumos");
    expect(list.at(1).text()).toBe("Harry Potter voted Lumos");
    expect(list.at(2).text()).toBe("Dumbledore voted Nox");
  });

  it("Shouldn't show dead players in player list", () => {
    const wrapper = wrap();
    const list = wrapper.find("div h4");
    expect(list.at(4).exists()).toBe(false);
  });
});

describe("Nomination Interface", () => {
  const store = createStore(reducers);
  function wrap() {
    return mount(
      <Provider store={store}>
        <Election
          playerList={{
            "Tom Riddle": { vote: "Lumos", isDead: false },
            "Harry Potter": { vote: "Lumos", isDead: false },
            Dumbledore: { vote: "Nox", isDead: false },
            "Severus Snape": { vote: "missing Vote", isDead: true },
          }}
          minister={"Tom Riddle"}
          director={"No director yet"}
          status={"nomination"}
          hand={["nox", "lumos", "nox"]}
          candidate={"Dumbledore"}
        />
      </Provider>
    );
  }
  store.getState().user = {
    username: "Tom Riddle",
    id: 1,
    token: 145,
    logged_in: true,
  };

  it("should show who's choosing proclamations", () => {
    const wrapper = wrap();
    const list = wrapper.find("div div h1");
    expect(list.text()).toBe("Minister Tom Riddle is nominating a Director...");
  });

  it("should show nomination button if you have are Minister", () => {
    const wrapper = wrap();
    const button = wrapper.find("div div button");
    expect(button.exists()).toBe(true);
  });

  it("shouldn't show nomination buttion if you are not Minister", () => {
    store.getState().user = {
      username: "Dumbledore",
      id: 3,
      token: 145,
      logged_in: true,
    };
    const wrapper = wrap();
    const button = wrapper.find("div div button");
    expect(button.exists()).toBe(false);
  });
});
