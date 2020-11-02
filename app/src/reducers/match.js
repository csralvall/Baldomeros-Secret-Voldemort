const matchReducer = (
  state = { id: -1, playerId: -1, name: "", hostId: -1 },
  action
) => {
  switch (action.type) {
    case "JOIN":
      return {
        id: action.payload.Match_id,
        playerId: action.payload.Player_id,
        hostId: action.payload.Host_id,
        name: action.payload.Match_name,
      };
    default:
      return state;
  }
};
export default matchReducer;
