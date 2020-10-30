const matchReducer = (
  state = { id: -1, playerId: -1, name: "",hostId:-1 },
  action
) => {
  switch (action.type) {
    case "JOIN":
      return {
        Match_id: action.payload.Match_id,
        Player_id: action.payload.Player_id,
        Host_id: action.payload.Host_id,
        Match_name: action.payload.Match_name
      };
    default:
      return state;
  }
};
export default matchReducer;
