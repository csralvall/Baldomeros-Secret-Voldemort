export const joinMatch = (matchData) => {
  return {
    type: "JOIN",
    payload: {
      Match_id: matchData.Match_id,
      Player_id: matchData.Player_id,
      Host_id: 1,
      Match_name: "Tom Riddle's game",
    },
  };
};
