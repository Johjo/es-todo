import type { FetchTodolistContract } from './hexagon/fetchTodolist.usecase.ts';
import type { OpenTaskContract } from './hexagon/openTask.usecase.ts';

export interface DependenciesUseCase {
  fetchTodolist(): FetchTodolistContract;
  openTask(): OpenTaskContract;
}
