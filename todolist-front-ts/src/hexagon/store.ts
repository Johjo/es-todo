import { configureStore } from '@reduxjs/toolkit';
import { todolistPageReducer } from './todolistPage.slice.ts';

export function createAppStore() {
  return configureStore({ reducer: { todolistPage: todolistPageReducer } });
}

const store = createAppStore();

export type RootState = ReturnType<typeof store.getState>;
export type AppStore = ReturnType<typeof createAppStore>;
