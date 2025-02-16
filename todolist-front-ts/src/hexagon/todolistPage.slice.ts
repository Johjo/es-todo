import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { RootState } from './store';

export type Task = { key: string, name: string };
export type TodolistPresentation = { statut: 'loading' } | { statut: 'empty' } | {
  statut: 'atLeastOneTask',
  tasks: Task[]
};

const initialState: TodolistPresentation = { statut: 'loading' };
export const todolistPageSlice = createSlice({
  name: 'todolist',
  initialState: initialState as TodolistPresentation,
  reducers: {
    todolistPageDisplayed: (_state, action: PayloadAction<TodolistPresentation>) => {
      return action.payload;
    }
  }
});


export const { todolistPageDisplayed } = todolistPageSlice.actions;
export const todolistPageReducer = todolistPageSlice.reducer

export const selectTodolistPage = (state: RootState) : TodolistPresentation => state.todolistPage as TodolistPresentation ;
