import { AppStore, createAppStore } from '../../hexagon/store';
import { expect } from 'vitest';
import { selectTodolistPage } from '../../hexagon/todolistPage.slice';
import { TodolistPageDisplayStore } from '../../secondary/todolistPageDisplayStore';

describe('todolistPageDisplayStore', () => {
  it('send todolist presentation to store', () => {
    const store: AppStore = createAppStore();
    const sut = new TodolistPageDisplayStore(store);
    sut.displayTodolistPage({ statut: 'empty' });


    const selector = selectTodolistPage(store.getState());
    expect(selector).toEqual({ statut: 'empty' });
  });
});
