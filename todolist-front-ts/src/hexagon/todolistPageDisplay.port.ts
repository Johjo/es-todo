import { TodolistPresentation } from './todolistPage.slice';
import { FromBackend } from './todolistPageDisplay.usecase';

export interface TodolistPageDisplayStorePort {
  displayTodolistPage(presentation: TodolistPresentation): void;
}

export interface TodolistFetcherPort {
  getTodolist(): Promise<FromBackend.Todolist>;
}
