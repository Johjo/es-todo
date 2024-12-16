import {AppStore, makeStore} from "@/lib/store";
import {NumberOfTasksFetched, TodolistPageState, WhichTaskFetched} from "@/lib/todolistPage.slice";
import {LoadTodolistPage} from "@/xxx/loadTodolistPage";
import {wait} from "next/dist/lib/wait";

export interface WhichTasksGateway {
    get(): Promise<any>;
}

class WhichTasksGatewayForTest implements WhichTasksGateway {
    private resultExpected: boolean = false;
    private tasks: any[];

    async get(): Promise<any> {
        if (this.resultExpected) {
            return this.tasks
        } else {
            console.log("waiting WhichTasksGatewayForTest")
            await wait(10000)
            console.log("waiting done")

        }
    }

    markAsOngoing() {
        this.resultExpected = false;
    }

    markAsCompleted(tasks: any[]) {
        this.resultExpected = true;
        this.tasks = tasks;
    }


}

export interface NumberOfTaskGateway {
    get(): Promise<any>;
}


class NumberOfTaskGatewayForTest implements NumberOfTaskGateway {
    private resultExpected: boolean = false;
    private numberOfTasks: number = 0;

    async get(): Promise<any> {
        if (this.resultExpected) {
            return this.numberOfTasks
        } else {
            console.log("waiting")
            await wait(10000)
            console.log("waiting done")
        }
    }

    markAsOngoing() {
        this.resultExpected = false;
    }

    markAsCompleted(numberOfTasks: number) {
        this.resultExpected = true;
        this.numberOfTasks = numberOfTasks;
    }
}

describe('LoadTodolistPage', () => {
    let store: AppStore;
    let otherInitialState: Omit<AppStore['getState'], 'todolistPage'>;
    let whichTasksGateway: WhichTasksGatewayForTest;
    let numberOfTaskGateway: NumberOfTaskGatewayForTest;

    beforeEach(() => {
        whichTasksGateway = new WhichTasksGatewayForTest();
        numberOfTaskGateway = new NumberOfTaskGatewayForTest();

        store = makeStore({whichTasksGateway, numberOfTaskGateway});
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
    });

    it('should tell there is no task', async () => {
        // GIVEN
        whichTasksGateway.markAsCompleted([]);

        // WHEN
        await store.dispatch(LoadTodolistPage())

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
        whichTasksGateway.markAsCompleted([{id: 1, name: "task1"}]);

        // WHEN
        await store.dispatch(LoadTodolistPage())

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
        whichTasksGateway.markAsCompleted([{id: 1, name: "task1"}, {id: 2, name: "task2"}]);

        // WHEN
        await store.dispatch(LoadTodolistPage())

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
        numberOfTaskGateway.markAsCompleted(17);

        // WHEN
        await store.dispatch(LoadTodolistPage())

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "loading"},
            tasksContext: {status: "loading"},
            numberOfTasks: {status: "idle", numberOfTasks: 17},
        });
    });
});