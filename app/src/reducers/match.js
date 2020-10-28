const matchReducer = (state = {id: 1, hostid:2, name: "Match1"}, action) => {
    switch (action.type) {
      case "JOIN":
        return action.payload;
      default:
        return state;
    }
  };
  export default matchReducer;
  