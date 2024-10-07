import {Task, WhichTask, WhichTaskQuery} from "@/hexagon/whichTaskQuery/whichTask.query";
import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";
import {Dependencies} from "@/primary/controller/dependencies";

export class ChooseTaskForTest implements ChooseAndIgnoreTask.Contract {
    private _history: undefined | [number, number] = undefined;

    execute(chosenTaskId: number, ignoredTaskId: number): void {
        this._history = [chosenTaskId, ignoredTaskId];
    }

    history() {
        assert(this._history !== undefined, 'history() called before execute()');
        return this._history;
    }
}

export class WhichTaskQueryForTest implements WhichTask.Contract {
    private _tasks: Task[] = [];

    query(): Task[] {
        return this._tasks;
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

export function injectAllUseCase(dependencies: Dependencies): Dependencies {
    return {
        ...dependencies,
        chooseAndIgnoreTask: {...dependencies.chooseAndIgnoreTask, useCase: ChooseAndIgnoreTask.build},
        whichTask: {...dependencies.whichTask, query: WhichTask.build},
    }
}