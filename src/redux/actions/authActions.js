import axios from 'axios';
import jwtDecode from 'jwt-decode';

export const login = (credentials) => async (dispatch) => {
  try {
    const response = await axios.post('/auth/login', credentials);
    const { access_token } = response.data;
    const user = jwtDecode(access_token);
    dispatch({ type: 'LOGIN_SUCCESS', payload: { user, token: access_token } });
  } catch (error) {
    dispatch({ type: 'LOGIN_FAILURE', payload: error.message });
  }
};