import { configureStore } from '@reduxjs/toolkit';
import { todolistPageReducer } from './todolistPage.slice.ts';
import { DependenciesUseCase } from '../dependenciesUseCase.ts';
import { DependenciesUseCaseDummy } from '../test/webapp/unit/todolist/primary/dependenciesUseCaseDummy.ts';

export function createAppStore(useCaseDependencies: DependenciesUseCase) {
  return configureStore({
      reducer: { todolistPage: todolistPageReducer },
      middleware: (getDefaultMiddleware) => getDefaultMiddleware({
        thunk: {
          extraArgument: useCaseDependencies
        }
      })
    }
  );
}

const store = createAppStore(new DependenciesUseCaseDummy() );

export type RootState = ReturnType<typeof store.getState>;
export type AppStore = ReturnType<typeof createAppStore>;
export type AppDispatch = typeof store.dispatch;
