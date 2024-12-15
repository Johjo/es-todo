import {AppStore, makeStore} from "@/lib/store";
import {NumberOfTasksFetched, TasksContextFetched, TodolistPageState, WhichTaskFetched} from "@/lib/todolistPage.slice";
import {LoadTodolistPage} from "@/xxx/loadTodolistPage";

describe('LoadTodolistPage', () => {
    let store: AppStore;
    let otherInitialState: Omit<AppStore['getState'], 'todolistPage'>;;

    beforeEach(() => {
        store = makeStore();
        const {todolistPage: _, ...rest} = store.getState();
        otherInitialState = rest;
    });
    it('should display todolist page loading when do nothing', async () => {
        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "loading"},
            tasksContext: {status: "loading"},
            numberOfTasks: {status: "loading"},
        });
    });

    it('should display todolist page loading when do nothing', async () => {
        // GIVEN

        // WHEN
        store.dispatch(LoadTodolistPage())

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "idle", type: "nothing to do"},
            tasksContext: {status: "idle"},
            numberOfTasks: {status: "idle"},
        });
    });


});