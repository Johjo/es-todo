import {AppStore, makeStore} from "@/lib/store";
import {NumberOfTasksFetched, TodolistPageState, WhichTaskFetched} from "@/lib/todolistPage.slice";
import {LoadTodolistPage} from "@/xxx/loadTodolistPage";
import {wait} from "next/dist/lib/wait";

export interface WhichTasksGateway {
    get(): Promise<any>;
}

class WhichTasksGatewayForTest implements WhichTasksGateway {
    private resultExpected: boolean = false;

    async get(): Promise<any> {
        if (this.resultExpected) {
            return []
        } else {
            console.log("waiting WhichTasksGatewayForTest")
            await wait(10000)
            console.log("waiting done")

        }
    }

    markAsOngoing() {
        this.resultExpected = false;
    }

    markAsCompleted() {
        this.resultExpected = true;
    }


}

export interface NumberOfTaskGateway {
    get(): Promise<any>;
}


class NumberOfTaskGatewayForTest implements NumberOfTaskGateway {
    private resultExpected: boolean = false;

    async get(): Promise<any> {
        if (this.resultExpected) {
            return 0
        } else {
            console.log("waiting")
            await wait(10000)
            console.log("waiting done")
        }
    }

    markAsOngoing() {
        this.resultExpected = false;
    }

    markAsCompleted() {
        this.resultExpected = true;
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
        whichTasksGateway.markAsCompleted();

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

    it('should tell number of task', async () => {
        // GIVEN
        numberOfTaskGateway.markAsCompleted();

        // WHEN
        await store.dispatch(LoadTodolistPage())

        // THEN
        const {todolistPage, ...otherState} = store.getState();

        expect(otherState).toStrictEqual({...otherInitialState});
        expect(todolistPage).toStrictEqual<TodolistPageState>({
            whichTasks: {status: "loading"},
            tasksContext: {status: "loading"},
            numberOfTasks: {status: "idle", numberOfTasks: 0},
        });
    });
});