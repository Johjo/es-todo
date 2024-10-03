import {createSlice, PayloadAction} from "@reduxjs/toolkit";

export type Task = {
    id: number,
    name: string,
}

export type Todolist = {
    tasks: Task[],
    contexts: string[],
    numberOfTasks: number
}

export type WhichTask ={
    tasks: Task[];
}

let initialState: Todolist = {numberOfTasks: 0, contexts: [], tasks: []};

export const todolistSlice = createSlice({
    name: "todolist",
    initialState,
    reducers: {
        todoListFetched(state, action: PayloadAction<Todolist>) {
            state.numberOfTasks = action.payload.numberOfTasks;
            state.contexts = action.payload.contexts;
            state.tasks = action.payload.tasks;
        },
        WhichTaskUpdated(state, action: PayloadAction<WhichTask>) {
            state.tasks = action.payload.tasks;
        }
    },
    selectors: {
        selectNumberOfTasks: (todolist) => todolist.numberOfTasks
    },
})

export let reducer = todolistSlice.reducer;
export const { todoListFetched, WhichTaskUpdated } = todolistSlice.actions;
export const { selectNumberOfTasks } = todolistSlice.selectors;