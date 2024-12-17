import {AppStore, makeStore} from "@/lib/store";
import {TodolistPageState} from "@/lib/todolistPage.slice";
import {LoadTodolistPage} from "@/xxx/loadTodolistPage";
import {wait} from "next/dist/lib/wait";

export interface WhichTasksGateway {
    get(): Promise<any>;
}

class WhichTasksGatewayForTest implements WhichTasksGateway {
    private response: any[] | undefined = undefined;

    async get(): Promise<any> {
        while (this.response === undefined) {
            await tic();
        }
        return this.response
    }

    feed(tasks: any[]) {
        this.response = tasks;
    }
}

export interface NumberOfTaskGateway {
    get(): Promise<number>;
}


export type NoResponse = "no response";

function tic() {
    return wait(10);
}

class NumberOfTaskGatewayForTest implements NumberOfTaskGateway {
    private response: number | undefined;

    async get(): Promise<number> {
        while (this.response === undefined) {
            await tic();
        }
        return this.response
    }

    feed(numberOfTasks: number) {
        this.response = numberOfTasks;
    }
}

export interface ContextGateway {
    get(): Promise<any>;
}

class ContextGatewayForTest implements ContextGateway {
    private response: string[] | undefined;

    async get(): Promise<any> {
        while (this.response === undefined) {
            await tic();
        }
        return this.response
    }

    feed(context: string[]) {
        this.response = context;
    }
}

describe('LoadTodolistPage', () => {
    let store: AppStore;
    let otherInitialState: Omit<AppStore['getState'], 'todolistPage'>;
    let whichTasksGateway: WhichTasksGatewayForTest;
    let numberOfTaskGateway: NumberOfTaskGatewayForTest;
    let contextGateway: ContextGatewayForTest;

    beforeEach(() => {
        whichTasksGateway = new WhichTasksGatewayForTest();
        numberOfTaskGateway = new NumberOfTaskGatewayForTest();
        contextGateway = new ContextGatewayForTest();

        store = makeStore({whichTasksGateway, numberOfTaskGateway, contextGateway});
        const {todolistPage: _, ...rest} = store.getState();
        otherInitialState = rest;
    });

    it('should tell every thing is loading', async () => {
        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "loading"},
            tasksContext: {status: "loading"},
            numberOfTasks: {status: "loading"},
        });
    });

    it('should tell everything is loading', async () => {
        // GIVEN

        // WHEN
        await store.dispatch(LoadTodolistPage())

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "loading"},
            tasksContext: {status: "loading"},
            numberOfTasks: {status: "loading"},
        });

        whichTasksGateway.feed([]);

        // FINISH
        whichTasksGateway.feed([]);
    });

    it('should tell there is no task', async () => {
        // GIVEN

        // WHEN
        await store.dispatch(LoadTodolistPage())
        whichTasksGateway.feed([]);
        await tic();

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "idle", type: "nothing to do"},
            tasksContext: {status: "loading"},
            numberOfTasks: {status: "loading"},
        });
    });

    it('should tell there is one task', async () => {
        // GIVEN

        // WHEN
        await store.dispatch(LoadTodolistPage())
        whichTasksGateway.feed([{id: 1, name: "task1"}]);
        await tic();

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "idle", type: "only one task"},
            tasksContext: {status: "loading"},
            numberOfTasks: {status: "loading"},
        });
    });

    it('should tell there is two tasks', async () => {
        // GIVEN

        // WHEN
        await store.dispatch(LoadTodolistPage())
        whichTasksGateway.feed([{id: 1, name: "task1"}, {id: 2, name: "task2"}]);
        await tic();

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "idle", type: "two tasks"},
            tasksContext: {status: "loading"},
            numberOfTasks: {status: "loading"},
        });
    });

    it('should tell number of task', async () => {
        // GIVEN


        // WHEN
        await store.dispatch(LoadTodolistPage())
        numberOfTaskGateway.feed(17);
        await tic();

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "loading"},
            tasksContext: {status: "loading"},
            numberOfTasks: {status: "idle", numberOfTasks: 17},
        });
    });

    it('should tell context and number of task', async () => {
        // GIVEN

        // WHEN
        await store.dispatch(LoadTodolistPage())

        numberOfTaskGateway.feed(17);
        contextGateway.feed(["#context1", "#context2"]);
        await tic();

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "loading"},
            tasksContext: {status: "idle", context: ["#context1", "#context2"]},
            numberOfTasks: {status: "idle", numberOfTasks: 17},
        });
    });

    it('should tell context', async () => {
        // GIVEN
        // WHEN

        await store.dispatch(LoadTodolistPage())
        contextGateway.feed(["#context1", "#context2"]);
        await tic();

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "loading"},
            tasksContext: {status: "idle", context: ["#context1", "#context2"]},
            numberOfTasks: {status: "loading"},
        });
    });
}, 100);