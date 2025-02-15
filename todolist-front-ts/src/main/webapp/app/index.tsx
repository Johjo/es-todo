import HomePage from '@/home/infrastructure/primary/HomePage';
import React from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import { BrowserRouter, Route, Routes } from 'react-router';

const container = document.getElementById('root');
const root = createRoot(container!);
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage/>} />
        {/*<Route path="/todolist/:key" element={<CoreTodolist/>} />*/}
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
);
