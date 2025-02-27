import { describe, expect, it } from 'vitest';
import { TaskForm, TodolistPage } from '../../../../../main/webapp/todolist/primary/TodolistPage.tsx';
import type { AppStore } from '../../../../../hexagon/store.ts';
import { createAppStore } from '../../../../../hexagon/store.ts';
import type { TodolistPageDisplayUseCase } from '../../../../../hexagon/todolistPageDisplay.usecase.ts';
import { renderWithDependencies } from './renderWithDependencies.tsx';
import { DependenciesUseCaseDummy } from './dependenciesUseCaseDummy.ts';
import { waitFor } from '@testing-library/dom';
import type { OpenTaskContract } from '../../../../../hexagon/openTask.usecase.ts';
import userEvent from '@testing-library/user-event';

describe('TodolistPage', () => {
  let store: AppStore;
  let renderBis: ReturnType<typeof renderWithDependencies>;
  let todolistPageDisplay: TodolistPageDisplayUseCaseForTest;
  let openTask: OpenTaskUseCaseForTest;

  beforeEach(() => {
    todolistPageDisplay = new TodolistPageDisplayUseCaseForTest();
    openTask = new OpenTaskUseCaseForTest();
    store = createAppStore({});
    renderBis = renderWithDependencies(store, new DependenciesUseCaseForTest(todolistPageDisplay, openTask));
  });

  describe('Should load todolist', () => {
    it('do nothing', () => {
      expect(todolistPageDisplay.hasBeenExecuted()).toBeFalsy();
    });

    it('after loading', () => {
      renderBis(<TodolistPage />);

      expect(todolistPageDisplay.hasBeenExecuted()).toBeTruthy();
    });

    it('click on button should open task', async () => {
      const { getByRole } = renderBis(<TaskForm />);
      const button = getByRole('button');
      const input = getByRole('textbox');

      await userEvent.type(input, 'Buy water');
      await userEvent.click(button);

      await waitFor(() => expect(openTask.hasBeenExecutedWith()).toEqual({ name: 'Buy water' }));
    });


  });
});

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
  constructor(private readonly _todolistPageDisplay: TodolistPageDisplayUseCaseForTest, private readonly _openTask: OpenTaskUseCaseForTest) {
    super();
  }

  todolistPageDisplay(): TodolistPageDisplayUseCase {
    return this._todolistPageDisplay;
  }

  openTask(): OpenTaskContract {
    return this._openTask;
  }

}


class OpenTaskUseCaseForTest implements OpenTaskContract {
  private _hasBeenExecuted: { name: string } | undefined = undefined;

  execute(taskName: string): Promise<void> {
    this._hasBeenExecuted = { name: taskName };
    return Promise.resolve();
  }

  hasBeenExecutedWith() {
    return this._hasBeenExecuted;
  }
}
