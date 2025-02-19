import HomePage from '@/home/infrastructure/primary/HomePage';
import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import { BrowserRouter, Route, Routes } from 'react-router';
import { TodolistPage } from '../todolist/primary/TodolistPage.tsx';
import { DependenciesContext } from '../todolist/primary/useDependenciesUseCase.ts';
import type { DependenciesUseCase } from '../todolist/primary/dependenciesUseCase.ts';
import type { TodolistPageDisplayUseCase } from 'src/hexagon/todolistPageDisplay.usecase.ts';
import { TodolistPageDisplayImpl } from 'src/hexagon/todolistPageDisplay.usecase.ts';
import { Provider } from 'react-redux';
import { AppStore, createStore } from '../../../hexagon/store.ts';
import type { TodolistFetcherPort, TodolistPageDisplayStorePort } from '../../../hexagon/todolistPageDisplay.port.ts';
import { TodolistPageDisplayStore } from '../../../secondary/todolistPageDisplayStore.ts';
import { TodolistFetcher } from '../../../secondary/todolistFetcher.ts';

const container = document.getElementById('root');

class DependenciesUseCaseImpl implements DependenciesUseCase {
  constructor(private readonly _adapters: DependenciesAdapter) {

  }

  todolistPageDisplay(): TodolistPageDisplayUseCase {
    const store: TodolistPageDisplayStorePort = this._adapters.todolistPageDisplayStore();
    const todolistFetcher: TodolistFetcherPort = this._adapters.todolistFetcher();

    return new TodolistPageDisplayImpl(store, todolistFetcher);
  }
}

class DependenciesAdapter {
  constructor(private readonly _store: AppStore) {
    this._store = store;

  }

  todolistPageDisplayStore() : TodolistPageDisplayStorePort {
    return new TodolistPageDisplayStore(this._store);
  }

  todolistFetcher() : TodolistFetcherPort {
    return new TodolistFetcher();
  }
}

const store : AppStore = createStore();
const useCaseDependencies: DependenciesUseCaseImpl = new DependenciesUseCaseImpl(new DependenciesAdapter(store));

const root = createRoot(container!);
root.render(
  <React.StrictMode>
    <DependenciesContext value={useCaseDependencies}>
      <Provider store={store}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/todolist" element={<TodolistPage />} />
            {/*<Route path="/todolist/:key" element={<CoreTodolist/>} />*/}
          </Routes>
        </BrowserRouter>
      </Provider>
    </DependenciesContext>
  </React.StrictMode>
);
