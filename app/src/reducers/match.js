const matchReducer = (
  state = { id: -1, playerId: -1, name: "", hostId: -1 },
  action
) => {
  switch (action.type) {
    case "JOIN":
      return action.payload;
    case "CREATE":
      return action.payload;
    default:
      return state;
  }
};
export default matchReducer;
