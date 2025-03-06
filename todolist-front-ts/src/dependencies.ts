import type { TodolistFetcherPort } from './hexagon/fetchTodolist.port.ts';
import type { OpenTaskUpdaterPort, UuidGeneratorPort } from './hexagon/openTask.port.ts';
import type { DependenciesUseCase } from './dependenciesUseCase.ts';
import type { AppDispatch } from './hexagon/store.ts';
import { FetchTodolistPrimaryPort, FetchTodolistUseCase } from './hexagon/fetchTodolist.usecase.ts';
import { OpenTaskPrimaryPort, OpenTaskUseCase } from './hexagon/openTask.usecase.ts';

export interface DependenciesAdapter {

  todolistFetcher(): TodolistFetcherPort;

  uuidGenerator(): UuidGeneratorPort;

  todolistUpdater(): OpenTaskUpdaterPort;
}

export class DependenciesUseCaseImpl implements DependenciesUseCase {
  constructor(private readonly adapters: DependenciesAdapter) {
  }

  fetchTodolist(dispatch: AppDispatch): FetchTodolistPrimaryPort {
    const todolistFetcher: TodolistFetcherPort = this.adapters.todolistFetcher();
    return new FetchTodolistUseCase(todolistFetcher, dispatch);
  }

  openTask(dispatch: AppDispatch): OpenTaskPrimaryPort {
    const uuidGenerator: UuidGeneratorPort = this.adapters.uuidGenerator();
    const todolistUpdater: OpenTaskUpdaterPort = this.adapters.todolistUpdater();
    return new OpenTaskUseCase(uuidGenerator, todolistUpdater, dispatch);
  }
}
