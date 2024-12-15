import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";
import {AppStore, AppThunk, makeStore} from "@/lib/store";

const thunkFunction = (dispatch, getState) => {
    // logic here that can dispatch actions or read state
}

export type ChooseAndIgnoreTaskFn = () => any;

export const chooseAndIgnoreTask: ChooseAndIgnoreTaskFn = (): AppThunk =>
    async (dispatch, getState, dependencies) => {
    };


describe('chooseTask', () => {
    it.each([
        [1, 3, {chosenTaskId: 1, ignoredTaskId: 3}],
        [2, 3, {chosenTaskId: 2, ignoredTaskId: 3}],
        [3, 1, {chosenTaskId: 3, ignoredTaskId: 1}],
    ])('should choose the task %s and ignore the task %s', async (chosenTaskId, ignoredTaskId, expected) => {
        let todolist = new TodolistForTest();
        let store: AppStore = makeStore();

        store.dispatch(chooseAndIgnoreTask());

        const sut = new ChooseAndIgnoreTask.UseCase({todolist});
        await sut.execute(chosenTaskId, ignoredTaskId)

        let actual = todolist.lastUpdate()
        expect(actual).toStrictEqual(expected);
    });
});


class TodolistForTest implements ChooseAndIgnoreTask.Port.Todolist {
    _lastUpdate: any

    lastUpdate() {
        return this._lastUpdate;
    }

    chooseAndIgnoreTask(chosenTaskId: number, ignoredTaskId: number) {
        this._lastUpdate = {chosenTaskId: chosenTaskId, ignoredTaskId: ignoredTaskId}
    }
}
