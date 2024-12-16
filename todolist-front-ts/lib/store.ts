import type { Action, ThunkAction } from "@reduxjs/toolkit";
import { combineSlices, configureStore } from "@reduxjs/toolkit";
import { counterSlice } from "./features/counter/counterSlice";
import { quotesApiSlice } from "./features/quotes/quotesApiSlice";
import {todolistSlice} from "@/lib/todolist.slice";
import {todolistPageSlice} from "@/lib/todolistPage.slice";
import {NumberOfTaskGateway, WhichTasksGateway} from "@/xxx/loadTodolistPage.spec";



// `combineSlices` automatically combines the reducers using
// their `reducerPath`s, therefore we no longer need to call `combineReducers`.
const rootReducer = combineSlices(counterSlice, todolistSlice, todolistPageSlice);
// Infer the `RootState` type from the root reducer
export type RootState = ReturnType<typeof rootReducer>;

// `makeStore` encapsulates the store configuration to allow
// creating unique store instances, which is particularly important for
// server-side rendering (SSR) scenarios. In SSR, separate store instances
export interface Dependencies {
  whichTasksGateway: WhichTasksGateway,
  numberOfTaskGateway: NumberOfTaskGateway,
}

// are needed for each request to prevent cross-request state pollution.
export const makeStore = (dependencies: Partial<Dependencies>) => {
  return configureStore({
    reducer: rootReducer,
    // Adding the api middleware enables caching, invalidation, polling,
    // and other useful features of `rtk-query`.
    middleware: (getDefaultMiddleware) => {
      return getDefaultMiddleware({thunk: {extraArgument: dependencies}});
    },
  });
};

// Infer the return type of `makeStore`
export type AppStore = ReturnType<typeof makeStore>;
// Infer the `AppDispatch` type from the store itself
export type AppDispatch = AppStore["dispatch"];
export type AppThunk<ThunkReturnType = void> = ThunkAction<
  ThunkReturnType,
  RootState,
  Dependencies,
  Action
>;
