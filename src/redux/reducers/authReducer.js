const initialState = {
  user: null,
  token: null,
  error: null,
};

const authReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'LOGIN_SUCCESS':
      return { ...state, user: action.payload.user, token: action.payload.token, error: null };
    case 'LOGIN_FAILURE':
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

export default authReducer;