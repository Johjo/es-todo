import { describe, it } from 'vitest';
import { act, render } from '@testing-library/react';
import { v4 } from 'uuid';
import { TodolistPage, TodolistPageDisplay } from '../../../../../main/webapp/todolist/primary/TodolistPage.tsx';
import type { AppStore } from '../../../../../hexagon/store.ts';
import { createStore } from '../../../../../hexagon/store.ts';
import { Provider } from 'react-redux';
import React from 'react';
import { todolistFetched } from '../../../../../hexagon/todolistPage.ts';


function aTask() {
  return { key: v4(), name: `buy the milk --- ${v4()} ---` };
}

const renderWithStore = (store: AppStore) => (ui: React.ReactElement) => render(<Provider
  store={store}>{ui}</Provider>);

describe('TodolistPage', () => {
  let store: AppStore;
  let renderBis: ReturnType<typeof renderWithStore>;
  beforeEach(() => {
    store = createStore();
    renderBis = renderWithStore(store);
  });

  describe('loading statut', () => {
    it('todolist is loading', () => {
      const { queryByText } = renderBis(<TodolistPageDisplay />);
      const text = queryByText('loading...');
      expect(text).toBeTruthy();
    });

    it('todolist is not loading', () => {
      const { queryByText } = renderBis(<TodolistPageDisplay />);
      act(() => {
        store.dispatch(todolistFetched({ tasks: [] }));
      });
      const text = queryByText('loading...');
      expect(text).toBeFalsy();
    });
  });

  describe('empty state statut', () => {
    it('after loading', () => {
      const { queryByText } = renderBis(<TodolistPageDisplay />);

      act(() => {
        store.dispatch(todolistFetched({ tasks: [] }));
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
        store.dispatch(todolistFetched({ tasks: [task] }));
      });

      const { getByText } = renderBis(<TodolistPageDisplay />);
      getByText(task.name);
    });

    it('many tasks', () => {
      const task_one = { ...aTask(), name: 'buy the milk' };
      const task_two = { ...aTask(), name: 'buy the bread' };

      const { getByText } = renderBis(<TodolistPageDisplay />);

      act(() => {
        store.dispatch(todolistFetched({ tasks: [task_one, task_two] }));
      });


      getByText(task_one.name);
      getByText(task_two.name);
    });
  });

  describe('Should load todolist', () => {
    it('after loading', () => {
      const { getByText } = renderBis(<TodolistPage />);

      getByText('no task...');
    });
  })
});


