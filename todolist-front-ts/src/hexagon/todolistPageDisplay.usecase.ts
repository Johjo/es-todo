import { TodolistFetcherPort } from './todolistPageDisplay.port';
import { emptyTodolistFetched, todolistFetched, todolistFetchingStarted } from './todolistPage.slice.ts';
import { AppStore } from './store.ts';

export interface TodolistPageDisplayUseCase {
  execute(): Promise<void>;
}

export class TodolistPageDisplayImpl implements TodolistPageDisplayUseCase {
  constructor(private readonly todolistFetcher: TodolistFetcherPort, private readonly store: AppStore) {
  }

  async execute(): Promise<void> {
    this.store.dispatch(todolistFetchingStarted());

    const todolist = await this.todolistFetcher.getTodolist('b69785c5-9266-486c-9655-52d85ad25bd5');

    if (todolist.tasks.length === 0) {
      this.store.dispatch(emptyTodolistFetched());
      return;
    }

    this.store.dispatch(todolistFetched(todolist.tasks));
  }
}

export namespace FromBackend {
  export type Task = { key: string, name: string };
  export type Todolist = { tasks: FromBackend.Task[] };
}
