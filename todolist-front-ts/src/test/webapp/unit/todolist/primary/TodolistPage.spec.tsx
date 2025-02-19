import { describe, expect, it } from 'vitest';
import { TodolistPage } from '../../../../../main/webapp/todolist/primary/TodolistPage.tsx';
import type { AppStore } from '../../../../../hexagon/store.ts';
import { createStore } from '../../../../../hexagon/store.ts';
import type { TodolistPageDisplayUseCase } from '../../../../../hexagon/todolistPageDisplay.usecase.ts';
import { renderWithDependencies } from './renderWithDependencies.tsx';
import { DependenciesUseCaseDummy } from './dependenciesUseCaseDummy.ts';

class TodolistPageDisplayUseCaseForTest implements TodolistPageDisplayUseCase {
  private _hasBeenExecuted: boolean = false;

  execute(): Promise<void> {
    this._hasBeenExecuted = true;
    return Promise.resolve();
  }

  hasBeenExecuted() {
    return this._hasBeenExecuted;
  }
}

class DependenciesUseCaseForTest extends DependenciesUseCaseDummy {
  constructor(private readonly _todolistPageDisplay: TodolistPageDisplayUseCaseForTest) {
    super();
  }

  todolistPageDisplay(): TodolistPageDisplayUseCase {
    return this._todolistPageDisplay;
  }
}

describe('TodolistPage', () => {
  let store: AppStore;
  let renderBis: ReturnType<typeof renderWithDependencies>;
  let todolistPageDisplay: TodolistPageDisplayUseCaseForTest;

  beforeEach(() => {
    todolistPageDisplay = new TodolistPageDisplayUseCaseForTest();
    store = createStore();
    renderBis = renderWithDependencies(store, new DependenciesUseCaseForTest(todolistPageDisplay));
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


