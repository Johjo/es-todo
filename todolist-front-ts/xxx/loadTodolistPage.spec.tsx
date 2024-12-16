import {AppStore, makeStore} from "@/lib/store";
import {NumberOfTasksFetched, TasksContextFetched, TodolistPageState, WhichTaskFetched} from "@/lib/todolistPage.slice";
import {LoadTodolistPage} from "@/xxx/loadTodolistPage";

export interface WhichTasksGateway {
    get(): Promise<any>;
}

class WhichTasksGatewayForTest implements WhichTasksGateway {
    async get(): Promise<any> {

    }

    feed(tasks: any[]) {

    }

}

describe('LoadTodolistPage', () => {
    let store: AppStore;
    let otherInitialState: Omit<AppStore['getState'], 'todolistPage'>;;
    let whichTasksGateway: WhichTasksGatewayForTest;

    beforeEach(() => {
        whichTasksGateway = new WhichTasksGatewayForTest();
        store = makeStore({whichTasksGateway});
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

    it('should display todolist page after loading', async () => {
        // GIVEN
        whichTasksGateway.feed([])
        // WHEN
        await store.dispatch(LoadTodolistPage())

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "idle", type: "nothing to do"},
            tasksContext: {status: "idle", context: []},
            numberOfTasks: {status: "idle", numberOfTasks: 0},
        });
    });

    it('should display which task to do after loading', async () => {
        // GIVEN
        // feed the stub which task

        // WHEN
        store.dispatch(LoadTodolistPage())

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "loading"},
            tasksContext: {status: "idle", context: []},
            numberOfTasks: {status: "idle", numberOfTasks: 0},
        });
    });


});