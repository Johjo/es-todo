import { TodolistFetcherPort, TodolistPageDisplayStorePort } from './todolistPageDisplay.port';

export interface TodolistPageDisplayUseCase {
  execute(): Promise<void>;
}

export class TodolistPageDisplayImpl implements TodolistPageDisplayUseCase {
  constructor(private readonly store: TodolistPageDisplayStorePort, private readonly todolistFetcher: TodolistFetcherPort) {
  }

  async execute(): Promise<void> {
    this.store.displayTodolistPage({ statut: 'loading' });

    const todolist = await this.todolistFetcher.getTodolist("b69785c5-9266-486c-9655-52d85ad25bd5");

    if (todolist.tasks.length === 0) {
      this.store.displayTodolistPage({ statut: 'empty' });
      return;
    }

    this.store.displayTodolistPage({ statut: 'atLeastOneTask', tasks: todolist.tasks });
  }
}

export namespace FromBackend {
  export type Task = { key: string, name: string };
  export type Todolist = { tasks: FromBackend.Task[] };
}
