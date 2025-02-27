import { FromBackend } from './todolistPageDisplay.usecase';

export interface TodolistFetcherPort {
  getTodolist(todolistKey: string): Promise<FromBackend.Todolist>;
}
