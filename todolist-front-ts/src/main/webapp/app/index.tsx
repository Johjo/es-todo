import HomePage from '@/home/infrastructure/primary/HomePage';
import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import { BrowserRouter, Route, Routes } from 'react-router';
import { TodolistPage } from '../todolist/primary/TodolistPage.tsx';
import { Provider } from 'react-redux';
import type { AppStore } from '../../../hexagon/store.ts';
import { createAppStore } from '../../../hexagon/store.ts';
import { DependenciesUseCaseImpl } from '../../../dependencies.ts';
import { DependenciesAdapterForDemo } from '../../../dependenciesAdapterForDemo.ts';

const container = document.getElementById('root');

const store: AppStore = createAppStore(new DependenciesUseCaseImpl(new DependenciesAdapterForDemo()));

const root = createRoot(container!);
root.render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/todolist" element={<TodolistPage />} />
          {/*<Route path="/todolist/:key" element={<CoreTodolist/>} />*/}
        </Routes>
      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);
