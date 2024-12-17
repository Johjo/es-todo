import {createSlice, PayloadAction} from "@reduxjs/toolkit";

export type WhichTasksLoaded = { status: "idle" } & (WithNoTask | WithOneTask | WithTwoTasks)
export type WithNoTask = { type: "nothing to do" }
export type WithOneTask = { type: "only one task", task: Task }
export type WithTwoTasks = { type: "two tasks", mainTask: Task, secondTask: Task }

export type NumberOfTaskLoaded = { status: "idle", numberOfTasks: number };
export type TaskContextLoaded = { status: "idle", context: string[] };
export type Loading = { status: "loading" };

export type TodolistPageState = {
    whichTasks: Loading | WhichTasksLoaded,
    tasksContext: Loading | TaskContextLoaded,
    numberOfTasks: Loading | NumberOfTaskLoaded,
}

let initialState: TodolistPageState = {
    whichTasks: {status: "loading"},
    tasksContext: {status: "loading"},
    numberOfTasks: {status: "loading"},
};

type TaskKey = string;

export type Task = {
    key: TaskKey,
    name: string,
}

export type WhichTaskPayload = {
    tasks: Task[];
}

type NumberOfTasksPayload = {
    numberOfTasks: number;
}

type TasksContextPayload = {
    context: string[];
}

export const todolistPageSlice = createSlice({
    name: "todolistPage",
    initialState,
    reducers: {
        WhichTaskFetched(state, action: PayloadAction<WhichTaskPayload>) {
            switch (action.payload.tasks.length) {
                case 0:
                    state.whichTasks = {
                        status: "idle",
                        type: "nothing to do"};
                    break;

                case 1:
                    state.whichTasks = {
                        status: "idle",
                        type: "only one task",
                        task: action.payload.tasks[0]
                    };
                    break;

                default:
                    state.whichTasks = {
                        status: "idle",
                        type: "two tasks",
                        mainTask: action.payload.tasks[0],
                        secondTask: action.payload.tasks[1]
                    };
                    break;
            }
        },
        TasksContextFetched(state, action: PayloadAction<TasksContextPayload>) {
            state.tasksContext = {status: "idle", context: action.payload.context};
        },
        NumberOfTasksFetched(state, action: PayloadAction<NumberOfTasksPayload>) {
            state.numberOfTasks = {status: "idle", numberOfTasks: action.payload.numberOfTasks};
        },
    },
    selectors: {},
})

export const {WhichTaskFetched, TasksContextFetched, NumberOfTasksFetched} = todolistPageSlice.actions;
export const {} = todolistPageSlice.selectors;