const loginReducer = (state = false, action) => {
  switch (action.type) {
    case "LOGIN":
      return action.payload.valid;
    default:
      return state;
  }
};
export default loginReducer;
