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
    todolistFetched: (_state, action: PayloadAction<{ tasks: Task[] }>) => {
      if (action.payload.tasks.length === 0) {
        return { statut: 'empty' };
      }
      return { statut: 'atLeastOneTask', tasks: action.payload.tasks };
    }
  }
});


export const { todolistFetched } = todolistPageSlice.actions;
export const todolistPageReducer = todolistPageSlice.reducer

export const selectTodolistPage = (state: RootState) : TodolistPresentation => state.todolistPage as TodolistPresentation ;
