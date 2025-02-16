import { configureStore } from '@reduxjs/toolkit';
import { todolistPageReducer } from './todolistPage.slice.ts';

export function createStore() {
  return configureStore({ reducer: { todolistPage: todolistPageReducer } });
}

const store = createStore();

export type RootState = ReturnType<typeof store.getState>;
export type AppStore = ReturnType<typeof createStore>;
