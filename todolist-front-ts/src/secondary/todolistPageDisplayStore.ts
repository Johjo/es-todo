import { TodolistPageDisplayStorePort } from '../hexagon/fetchTodolist.port';
import { AppStore } from '../hexagon/store';
import { todolistPageDisplayed, TodolistPresentation } from '../hexagon/todolistPage.slice';

export class TodolistPageDisplayStore implements TodolistPageDisplayStorePort {
  constructor(private readonly _store: AppStore) {

  }

  displayTodolistPage(presentation: TodolistPresentation): void {
    this._store.dispatch(todolistPageDisplayed(presentation));
  }
}
