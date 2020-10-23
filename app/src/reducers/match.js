const matchReducer = (state = {id: 0, hostid:0, userlist : [], name: ""}, action) => {
    switch (action.type) {
      case "JOIN":
        return action.payload;
      default:
        return state;
    }
  };
  export default matchReducer;
  