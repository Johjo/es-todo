import { TodolistFetcherPort } from './fetchTodolist.port.ts';
import { emptyTodolistFetched, todolistFetched, todolistFetchingStarted } from './todolistPage.slice.ts';
import { DependenciesUseCase } from '../dependenciesUseCase.ts';
import { Action, ThunkAction } from '@reduxjs/toolkit';
import { AppDispatch, RootState } from './store.ts';

export interface FetchTodolistPrimaryPort {
  execute(): Promise<void>;
}

export class FetchTodolistUseCase implements FetchTodolistPrimaryPort {
  constructor(private readonly todolistFetcher: TodolistFetcherPort, private readonly dispatch: AppDispatch) {
  }

  async execute(): Promise<void> {
    this.dispatch(todolistFetchingStarted());

    const todolist = await this.todolistFetcher.getTodolist('b69785c5-9266-486c-9655-52d85ad25bd5');

    if (todolist.tasks.length === 0) {
      this.dispatch(emptyTodolistFetched());
      return;
    }

    this.dispatch(todolistFetched(todolist.tasks));
  }
}

export namespace FromBackend {
  export type Task = { key: string, name: string };
  export type Todolist = { tasks: FromBackend.Task[] };
}

export const fetchTodolist = (): ThunkAction<Promise<void>, RootState, DependenciesUseCase, Action> => async (dispatch: AppDispatch, _getState: any, useCase: DependenciesUseCase) => {
  await useCase.fetchTodolist(dispatch).execute();
};
