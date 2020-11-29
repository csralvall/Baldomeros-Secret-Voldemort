const matchReducer = (
  state = { id: -1, playerId: -1, name: "", hostName: "" },
  action
) => {
  switch (action.type) {
    case "JOIN":
      return action.payload;
    case "CREATE":
      return action.payload;
    case "LEAVE":
      return action.payload;
    default:
      return state;
  }
};
export default matchReducer;
