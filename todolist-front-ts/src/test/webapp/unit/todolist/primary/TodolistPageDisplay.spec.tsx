import { describe, it } from 'vitest';
import { act } from '@testing-library/react';
import { v4 } from 'uuid';
import { TodolistPageDisplay } from '../../../../../main/webapp/todolist/primary/TodolistPage.tsx';
import type { AppStore } from '../../../../../hexagon/store.ts';
import { createAppStore } from '../../../../../hexagon/store.ts';
import { todolistFetchingStarted, todolistPageDisplayed } from '../../../../../hexagon/todolistPage.slice.ts';
import { renderWithDependencies } from './renderWithDependencies.tsx';
import { DependenciesUseCaseDummy } from '../../../../dependenciesUseCaseDummy.ts';


function aTask() {
  return { key: v4(), name: `buy the milk --- ${v4()} ---` };
}


describe('TodolistPage Display', () => {
  let store: AppStore;
  let renderBis: ReturnType<typeof renderWithDependencies>;

  beforeEach(() => {
    store = createAppStore(new DependenciesUseCaseDummy());
    renderBis = renderWithDependencies(store);
  });

  describe('loading statut', () => {
    it('todolist is loading', () => {
      const { queryByText } = renderBis(<TodolistPageDisplay />);
      act(() => {
        store.dispatch(todolistFetchingStarted());
      });

      const text = queryByText('loading...');
      expect(text).toBeTruthy();
    });

    it('todolist is not loading', () => {
      const { queryByText } = renderBis(<TodolistPageDisplay />);
      act(() => {
        store.dispatch(todolistPageDisplayed({ statut: 'empty' }));
      });
      const text = queryByText('loading...');
      expect(text).toBeFalsy();
    });
  });

  describe('empty state statut', () => {
    it('after loading', () => {
      const { queryByText } = renderBis(<TodolistPageDisplay />);

      act(() => {
        store.dispatch(todolistPageDisplayed({ statut: 'empty' }));
      });

      const text = queryByText('no task...');
      expect(text).toBeTruthy();
    });

    it('while loading', () => {
      const { queryByText } = renderBis(<TodolistPageDisplay />);
      const text = queryByText('no task...');
      expect(text).toBeFalsy();
    });
  });

  describe('with tasks', () => {
    it('one task', () => {
      const task = aTask();

      act(() => {
        store.dispatch(todolistPageDisplayed({ statut: 'atLeastOneTask', tasks: [task] }));
      });

      const { getByText } = renderBis(<TodolistPageDisplay />);
      getByText(task.name);
    });

    it('many tasks', () => {
      const task_one = { ...aTask(), name: 'buy the milk' };
      const task_two = { ...aTask(), name: 'buy the bread' };

      const { getByText } = renderBis(<TodolistPageDisplay />);

      act(() => {
        store.dispatch(todolistPageDisplayed({ statut: 'atLeastOneTask', tasks: [task_one, task_two] }));
      });


      getByText(task_one.name);
      getByText(task_two.name);
    });
  });
});
