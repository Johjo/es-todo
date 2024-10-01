import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {counterSlice} from "@/lib/features/counter/counterSlice";

export type Todolist = {
    contexts: string[],
    numberOfTasks: number
}

type FetchedTodolist = {
    contexts: string[],
    numberOfTasks: number
}


let initialState: Todolist = {numberOfTasks: 0, contexts: []};

export const todolistSlice = createSlice({
    name: "todolist",
    initialState,
    reducers: {
        todoListFetched(state, action: PayloadAction<FetchedTodolist>) {
            state.numberOfTasks = action.payload.numberOfTasks;
            state.contexts = action.payload.contexts;
        }
    },
    selectors: {
        selectNumberOfTasks: (todolist) => todolist.numberOfTasks
    },
})

export let reducer = todolistSlice.reducer;
export const { todoListFetched } = todolistSlice.actions;
export const { selectNumberOfTasks } = todolistSlice.selectors;