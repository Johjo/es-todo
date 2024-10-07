import {Task, WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";
import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";

export class ChooseTaskForTest implements ChooseAndIgnoreTask.Contract {
    private _history: undefined | [number, number] = undefined;

    execute(chosenTaskId: number, ignoredTaskId: number) : Promise<void> {
        this._history = [chosenTaskId, ignoredTaskId];
        return Promise.resolve();
    }

    history() {
        assert(this._history !== undefined, 'history() called before execute()');
        return this._history;
    }
}

export class WhichTaskQueryForTest implements WhichTask.Contract {
    private _tasks: Task[] = [];

    query(): Promise<Task[]> {
        return Promise.resolve(this._tasks);
    }

    feed(tasks: Task[]) {
        this._tasks = tasks;
    }
}

export class StoreForTest {
    _history: any[] = [];

    history(): any[] {
        return this._history
    }

    dispatch(expectedElement: any) {
        this._history.push(expectedElement);
    }
}

