import {ChooseTaskUseCase, ScreenPort, TodolistPort} from "@/hexagon/chooseTask.usecase";


describe('chooseTask', () => {
    it.each([
        [1, 3, {chosenTaskId: 1, ignoredTaskId: 3}],
        [2, 3, {chosenTaskId: 2, ignoredTaskId: 3}],
        [3, 1, {chosenTaskId: 3, ignoredTaskId: 1}],
    ])('should choose the task %s and ignore the task %s', (chosenTaskId, ignoredTaskId, expected) => {
        let todolist = new TodolistForTest();

        const sut = new ChooseTaskUseCase(todolist, new ScreenForTest())
        sut.execute(chosenTaskId, ignoredTaskId)

        let actual = todolist.lastUpdate()
        expect(actual).toStrictEqual(expected);
    });

    it('should refresh tasks when choosing a task', () => {
        const screen = new ScreenForTest();
        const sut = new ChooseTaskUseCase(new TodolistForTest(), screen)

        sut.execute(1, 3)

        expect(screen.statusScreen).toBe("updated");
    });

    it('should update todolist then refresh screen', () => {
        const spy = new Spy();
        const sut = new ChooseTaskUseCase(spy, spy)

        sut.execute(1, 3)

        expect(spy.history()).toStrictEqual([
            "todolist updated",
            "screen refreshed"
        ]);

    });


});


class TodolistForTest implements TodolistPort {
    _lastUpdate: any

    lastUpdate() {
        return this._lastUpdate;
    }

    chooseAndIgnoreTask(chosenTaskId: number, ignoredTaskId: number) {
        this._lastUpdate = {chosenTaskId: chosenTaskId, ignoredTaskId: ignoredTaskId}
    }
}

class ScreenForTest implements ScreenPort {
    statusScreen: string = "";

    refreshTasks() {
        this.statusScreen = "updated";
    }
}

class Spy implements TodolistPort, ScreenPort {
    private _history: string[] = [];

    refreshTasks() {
        this._history.push("screen refreshed");
    }

    chooseAndIgnoreTask(_chosenTaskId: number, _ignoredTaskId: number) {
        this._history.push("todolist updated");
    }

    history() {
        return this._history;
    }
}
