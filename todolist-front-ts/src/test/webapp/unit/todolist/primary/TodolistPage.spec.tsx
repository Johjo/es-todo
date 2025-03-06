import { describe, expect, it } from 'vitest';
import { TaskForm, TodolistPage } from '../../../../../main/webapp/todolist/primary/TodolistPage.tsx';
import type { AppStore } from '../../../../../hexagon/store.ts';
import { createAppStore } from '../../../../../hexagon/store.ts';
import type { FetchTodolistPrimaryPort } from '../../../../../hexagon/fetchTodolist.usecase.ts';
import { renderWithDependencies } from './renderWithDependencies.tsx';
import { waitFor } from '@testing-library/dom';
import type { OpenTaskPrimaryPort } from '../../../../../hexagon/openTask.usecase.ts';
import userEvent from '@testing-library/user-event';

import { DependenciesUseCaseDummy } from '../../../../dependenciesUseCaseDummy.ts';

class DependenciesUseCaseForTest extends DependenciesUseCaseDummy {
  constructor(private readonly _fetchTodolist: FetchTodolistPrimaryPort, private readonly _openTask: OpenTaskPrimaryPort) {
    super();
  }

  fetchTodolist(): FetchTodolistPrimaryPort {
    return this._fetchTodolist;
  }

  openTask(): OpenTaskPrimaryPort {
    return this._openTask;
  }
}

describe('TodolistPage', () => {
  let store: AppStore;
  let renderBis: ReturnType<typeof renderWithDependencies>;
  let fetchTodolist: TodolistPageDisplayUseCaseForTest;
  let openTask: OpenTaskUseCaseForTest;

  beforeEach(() => {
    fetchTodolist = new TodolistPageDisplayUseCaseForTest();
    openTask = new OpenTaskUseCaseForTest();
    store = createAppStore(new DependenciesUseCaseForTest(fetchTodolist, openTask));
    renderBis = renderWithDependencies(store);
  });

  describe('Should load todolist', () => {
    it('do nothing', () => {
      expect(fetchTodolist.hasBeenExecuted()).toBeFalsy();
    });

    it('after loading', async () => {
      renderBis(<TodolistPage />);

      await waitFor(() => {

        expect(fetchTodolist.hasBeenExecuted()).toBeTruthy();
      });
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

class TodolistPageDisplayUseCaseForTest implements FetchTodolistPrimaryPort {
  private _hasBeenExecuted: boolean = false;

  execute(): Promise<void> {
    this._hasBeenExecuted = true;
    return Promise.resolve();
  }

  hasBeenExecuted() {
    return this._hasBeenExecuted;
  }
}

class OpenTaskUseCaseForTest implements OpenTaskPrimaryPort {
  private _hasBeenExecuted: { name: string } | undefined = undefined;

  execute(taskName: string): Promise<void> {
    this._hasBeenExecuted = { name: taskName };
    return Promise.resolve();
  }

  hasBeenExecutedWith() {
    return this._hasBeenExecuted;
  }
}
