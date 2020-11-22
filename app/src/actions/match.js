export const joinMatch = (matchData) => {
  return {
    type: "JOIN",
    payload: {
      id: matchData.Match_id,
      playerId: matchData.Player_id,
      hostName: matchData.Host_Name,
      name: matchData.Host_Name + "'s Game",
    },
  };
};
export const createMatchAction = (matchData) => {
  return {
    type: "CREATE",
    payload: {
      id: matchData.Match_id,
      playerId: matchData.Player_id,
      hostName: matchData.Host_Name,
      name: matchData.Host_Name + "'s Game",
    },
  };
};
