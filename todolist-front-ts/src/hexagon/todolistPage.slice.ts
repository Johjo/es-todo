import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from './store';

export type Task = { key: string, name: string };
export type TodolistPresentation =
  { statut: 'idle' } |
  { statut: 'loading' } |
  { statut: 'empty' } |
  {
    statut: 'atLeastOneTask',
    tasks: Task[]
  };

const initialState: TodolistPresentation = { statut: 'idle' };
export const todolistPageSlice = createSlice({
  name: 'todolist',
  initialState: initialState as TodolistPresentation,
  reducers: {
    todolistPageDisplayed: (_state, action: PayloadAction<TodolistPresentation>) => {
      return action.payload;
    },
    todolistFetchingStarted: (_state) => {
      return { statut: 'loading' };
    },
    emptyTodolistFetched: (_state) => {
      return { statut: 'empty' };
    },
    todolistFetched: (_state, action: PayloadAction<Task[]>) => {
      return { statut: 'atLeastOneTask', tasks: action.payload };
    }
  }
});


export const {
  todolistPageDisplayed,
  todolistFetchingStarted,
  emptyTodolistFetched,
  todolistFetched
} = todolistPageSlice.actions;
export const todolistPageReducer = todolistPageSlice.reducer;

export const selectTodolistPage = (state: RootState): TodolistPresentation => state.todolistPage as TodolistPresentation;
