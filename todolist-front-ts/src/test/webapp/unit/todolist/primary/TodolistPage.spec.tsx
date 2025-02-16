import { describe, expect, it } from 'vitest';
import { TodolistPage } from '../../../../../main/webapp/todolist/primary/TodolistPage.tsx';
import type { AppStore } from '../../../../../hexagon/store.ts';
import { createStore } from '../../../../../hexagon/store.ts';
import { TodolistPageDisplayUseCase } from '../../../../../hexagon/todolistPageDisplay.usecase.ts';
import { renderWithDependencies } from './renderWithDependencies.tsx';

class TodolistPageDisplayUseCaseForTest implements TodolistPageDisplayUseCase {
  private _hasBeenExecuted: boolean = false;

  async execute(): Promise<void> {
    this._hasBeenExecuted = true;
  }

  hasBeenExecuted() {
    return this._hasBeenExecuted;
  }
}

describe('TodolistPage', () => {
  let store: AppStore;
  let renderBis: ReturnType<typeof renderWithDependencies>;
  let todolistPageDisplay: TodolistPageDisplayUseCaseForTest;

  beforeEach(() => {
    todolistPageDisplay = new TodolistPageDisplayUseCaseForTest();
    store = createStore();
    renderBis = renderWithDependencies(store, { todolistPageDisplay });
  });

  describe('Should load todolist', () => {
    it('do nothing', () => {
      expect(todolistPageDisplay.hasBeenExecuted()).toBeFalsy();
    });

    it('after loading', () => {
      renderBis(<TodolistPage />);

      expect(todolistPageDisplay.hasBeenExecuted()).toBeTruthy();
    });
  });
});


