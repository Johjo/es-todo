import type { FetchTodolistPrimaryPort } from './hexagon/fetchTodolist.usecase.ts';
import type { OpenTaskPrimaryPort } from './hexagon/openTask.usecase.ts';
import type { AppDispatch } from './hexagon/store.ts';

export interface DependenciesUseCase {
  fetchTodolist(dispatch: AppDispatch): FetchTodolistPrimaryPort;
  openTask(dispatch: AppDispatch): OpenTaskPrimaryPort;
}
