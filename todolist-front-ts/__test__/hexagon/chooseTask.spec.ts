import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";

describe('chooseTask', () => {
    it.each([
        [1, 3, {chosenTaskId: 1, ignoredTaskId: 3}],
        [2, 3, {chosenTaskId: 2, ignoredTaskId: 3}],
        [3, 1, {chosenTaskId: 3, ignoredTaskId: 1}],
    ])('should choose the task %s and ignore the task %s', (chosenTaskId, ignoredTaskId, expected) => {
        let todolist = new TodolistForTest();

        const sut = new ChooseAndIgnoreTask.UseCase(todolist);
        sut.execute(chosenTaskId, ignoredTaskId)

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
