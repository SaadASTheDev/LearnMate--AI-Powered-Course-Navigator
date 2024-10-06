// File: frontend/store.js

import { configureStore, createSlice } from '@reduxjs/toolkit';

// Define the initial state for user interactions
const initialState = {
  userId: null,
  favorites: [],
  bookmarks: [],
};

// Create a slice for user interactions
const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setUserId: (state, action) => {
      state.userId = action.payload;
    },
    addToFavorites: (state, action) => {
      if (!state.favorites.includes(action.payload)) {
        state.favorites.push(action.payload);
      }
    },
    removeFromFavorites: (state, action) => {
      state.favorites = state.favorites.filter((courseId) => courseId !== action.payload);
    },
    addToBookmarks: (state, action) => {
      if (!state.bookmarks.includes(action.payload)) {
        state.bookmarks.push(action.payload);
      }
    },
    removeFromBookmarks: (state, action) => {
      state.bookmarks = state.bookmarks.filter((courseId) => courseId !== action.payload);
    },
  },
});

// Export actions for use in components
export const {
  setUserId,
  addToFavorites,
  removeFromFavorites,
  addToBookmarks,
  removeFromBookmarks,
} = userSlice.actions;

// Configure the Redux store
const store = configureStore({
  reducer: {
    user: userSlice.reducer,
  },
});

export default store;