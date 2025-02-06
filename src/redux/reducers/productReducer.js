const initialState = {
  items: [],
  error: null,
};

const productReducer = (state = initialState, action) => {
  switch (action.type) {
    case 'FETCH_PRODUCTS_SUCCESS':
      return { ...state, items: action.payload, error: null };
    case 'FETCH_PRODUCTS_FAILURE':
      return { ...state, error: action.payload };
    default:
      return state;
  }
};

export default productReducer;