import { configureStore } from '@reduxjs/toolkit';
import { todolistPageReducer } from './todolistPage.slice.ts';
import { OpenTaskContract } from './openTask.usecase.ts';

export type UseCases = {
  openTask: OpenTaskContract;
}

export function createAppStore(useCases : UseCases) {
  return configureStore({
      reducer: { todolistPage: todolistPageReducer },
      middleware: (getDefaultMiddleware) => getDefaultMiddleware({
        thunk: {
          extraArgument: useCases
        }
      })
    }
  );
}

const store = createAppStore({});

export type RootState = ReturnType<typeof store.getState>;
export type AppStore = ReturnType<typeof createAppStore>;
export type AppDispatch = ReturnType<typeof createAppStore>['dispatch'];
export type AppGetState = ReturnType<typeof store.getState>;
