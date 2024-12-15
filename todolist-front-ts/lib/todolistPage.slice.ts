import {createSlice} from "@reduxjs/toolkit";

export type TodolistPageState = {
    whichTasks: {status: "loading"},
    tasksContext: {status: "loading"},
    numberOfTasks: {status: "loading"},
}

let initialState: TodolistPageState = {
    whichTasks: {status: "loading"},
    tasksContext: {status: "loading"},
    numberOfTasks: {status: "loading"},
};

export const todolistPageSlice = createSlice({
    name: "todolistPage",
    initialState,
    reducers: {},
    selectors: {},
})

export let reducer = todolistPageSlice.reducer;
export const {} = todolistPageSlice.actions;
export const {} = todolistPageSlice.selectors;