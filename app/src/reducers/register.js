const registerReducer = (state = 0, action) => {
  switch (action.type) {
    case "REGISTER":
      return state;
    default:
      return state;
  }
};
export default registerReducer;
