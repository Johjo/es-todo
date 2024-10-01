import {createSlice, PayloadAction} from "@reduxjs/toolkit";
import {counterSlice} from "@/lib/features/counter/counterSlice";

export type Todolist = {
    numberOfTasks: number
}

type FetchedTodolist = {
    numberOfTasks: number
}


let initialState: Todolist = {numberOfTasks: 0};

export const todolistSlice = createSlice({
    name: "todolist",
    initialState,
    reducers: {
        todoListFetched(state, action: PayloadAction<FetchedTodolist>) {
            state.numberOfTasks = action.payload.numberOfTasks;
        }
    },
    selectors: {
        selectNumberOfTasks: (todolist) => todolist.numberOfTasks
    },
})

export let reducer = todolistSlice.reducer;
export const { todoListFetched } = todolistSlice.actions;
export const { selectNumberOfTasks } = todolistSlice.selectors;