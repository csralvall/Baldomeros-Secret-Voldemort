const storeMatchReducer = (
  state = { Match_id: -1, Player_id: -1 },
  action
) => {
  switch (action.type) {
    case "STORE_MATCH":
      return {
        Match_id: action.payload.Match_id,
        Player_id: action.payload.Player_id,
      };
    default:
      return state;
  }
};
export default storeMatchReducer;
