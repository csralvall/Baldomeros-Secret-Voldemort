export const joinMatch = (matchData) => {
  return {
    type: "JOIN",
    payload: {
      id: matchData.Match_id,
      playerId: matchData.Player_id,
      hostId: -1,
      name: "Tom Riddle's Game",
    },
  };
};
export const createMatchAction = (matchData) => {
  return {
    type: "CREATE",
    payload: {
      id: matchData.Match_id,
      playerId: matchData.Player_id,
      hostId: matchData.Host_id,
      name: "Tom Riddle's Game",
    },
  };
};
