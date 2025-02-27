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
import type { AppStore} from '../../../hexagon/store.ts';
import { createAppStore } from '../../../hexagon/store.ts';
import type { TodolistFetcherPort } from '../../../hexagon/todolistPageDisplay.port.ts';
import { TodolistFetcherHttp } from '../../../secondary/todolistFetcherHttp.ts';
import { OpenTaskContract, OpenTaskUseCase } from 'src/hexagon/openTask.usecase.ts';
import type { TodolistUpdaterPort, UuidGeneratorPort } from '../../../hexagon/openTask.port.ts';
import { UuidGeneratorRandom } from '../../../secondary/uuidGeneratorRandom.ts';
import { TodolistUpdaterHttp } from '../../../secondary/todolistUpdaterHttp.ts';

const container = document.getElementById('root');

class DependenciesUseCaseImpl implements DependenciesUseCase {
  constructor(private readonly _adapters: DependenciesAdapter) {

  }

  openTask(): OpenTaskContract {
    const uuidGenerator: UuidGeneratorPort = this._adapters.uuidGenerator();
    const todolistUpdater: TodolistUpdaterPort = this._adapters.todolistUpdater();
    return new OpenTaskUseCase(uuidGenerator, todolistUpdater, this._adapters.store());
  }

  todolistPageDisplay(): TodolistPageDisplayUseCase {
    const store: AppStore = this._adapters.store();
    const todolistFetcher: TodolistFetcherPort = this._adapters.todolistFetcher();

    return new TodolistPageDisplayImpl(todolistFetcher, store);
  }
}

class DependenciesAdapter {
  constructor(private readonly _store: AppStore) {
    this._store = store;

  }

  todolistFetcher(): TodolistFetcherPort {
    return new TodolistFetcherHttp('https://todolist-ytreza-dev.osc-fr1.scalingo.io');
    // return new TodolistFetcherHttp('http://127.0.0.1:8000');
  }

  store(): AppStore {
    return this._store;
  }

  uuidGenerator() : UuidGeneratorPort {
    return new UuidGeneratorRandom();
  }

  todolistUpdater() : TodolistUpdaterPort {
    return new TodolistUpdaterHttp('https://todolist-ytreza-dev.osc-fr1.scalingo.io');
  }
}

const store: AppStore = createAppStore();
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
