import { FromBackend } from './fetchTodolist.usecase.ts';

export interface TodolistFetcherPort {
  getTodolist(todolistKey: string): Promise<FromBackend.Todolist>;
}
