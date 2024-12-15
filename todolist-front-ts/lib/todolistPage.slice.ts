import {createSlice, PayloadAction} from "@reduxjs/toolkit";


export type WhichTasksLoaded = {status: "idle", type: "nothing to do" | "only one task" | "two tasks"}
export type NumberOfTaskLoaded = { status: "idle", numberOfTasks: number };

export type TodolistPageState = {
    whichTasks: { status: "loading" }  | WhichTasksLoaded,
    tasksContext: { status: "loading" | "idle" },
    numberOfTasks: { status: "loading" } | NumberOfTaskLoaded,
}

let initialState: TodolistPageState = {
    whichTasks: {status: "loading"},
    tasksContext: {status: "loading"},
    numberOfTasks: {status: "loading"},
};

type TaskKey = string;

type Task = {
    key: TaskKey,
    name: string,
}

export type WhichTaskPayload = {
    tasks: Task[];
}

type NumberOfTasksPayload = {
    numberOfTasks: number;
}

export const todolistPageSlice = createSlice({
    name: "todolistPage",
    initialState,
    reducers: {
        WhichTaskFetched(state, action: PayloadAction<WhichTaskPayload>) {
            switch (action.payload.tasks.length) {
                case 0:
                    state.whichTasks = {status: "idle", type: "nothing to do"};
                    break;
                case 1:
                    state.whichTasks = {status: "idle", type: "only one task"};
                    break;

                case 2:
                    state.whichTasks = {status: "idle", type: "two tasks"};
                    break;
            }
        },
        TasksContextFetched(state) {
            state.tasksContext = {status: "idle"};
        },
        NumberOfTasksFetched(state, action: PayloadAction<NumberOfTasksPayload>) {
            state.numberOfTasks = {status: "idle", numberOfTasks: action.payload.numberOfTasks};
        },
    },
    selectors: {},
})

export let reducer = todolistPageSlice.reducer;
export const {WhichTaskFetched, TasksContextFetched, NumberOfTasksFetched} = todolistPageSlice.actions;
export const {} = todolistPageSlice.selectors;