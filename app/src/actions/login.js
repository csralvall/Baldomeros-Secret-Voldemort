export const login = (data) => {
  return {
    type: "LOGIN",
    payload: {valid : data}
  };
};
