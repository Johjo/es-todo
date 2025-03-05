import { TodolistFetcherPort } from './fetchTodolist.port.ts';
import { emptyTodolistFetched, todolistFetched, todolistFetchingStarted } from './todolistPage.slice.ts';
import { DependenciesUseCase } from '../dependenciesUseCase.ts';
import { Action, ThunkAction } from '@reduxjs/toolkit';
import { RootState } from './store.ts';

export interface FetchTodolistContract {
  execute(dispatch: any): Promise<void>;
}

export class FetchTodolistUseCase implements FetchTodolistContract {
  constructor(private readonly todolistFetcher: TodolistFetcherPort) {
  }

  async execute(dispatch: any): Promise<void> {
    dispatch(todolistFetchingStarted());

    const todolist = await this.todolistFetcher.getTodolist('b69785c5-9266-486c-9655-52d85ad25bd5');

    if (todolist.tasks.length === 0) {
      dispatch(emptyTodolistFetched());
      return;
    }

    dispatch(todolistFetched(todolist.tasks));
  }
}

export namespace FromBackend {
  export type Task = { key: string, name: string };
  export type Todolist = { tasks: FromBackend.Task[] };
}

export const fetchTodolist = (): ThunkAction<Promise<void>, RootState, DependenciesUseCase, Action> => async (dispatch: any, _getState: any, dependenciesUseCase: DependenciesUseCase) => {
  const fetchTodolist = dependenciesUseCase.fetchTodolist();
  await fetchTodolist.execute(dispatch);
};
