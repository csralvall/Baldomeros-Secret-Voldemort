const signUpReducer = (state = false, action) => {
  switch (action.type) {
    case "SIGN_UP":
      return !state;
    default:
      return state;
  }
};
export default signUpReducer;
