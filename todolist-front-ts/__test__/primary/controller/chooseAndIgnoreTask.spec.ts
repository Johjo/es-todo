import {WhichTaskUpdated} from "@/lib/todolist.slice";
import {WhichTask, Task} from "@/hexagon/whichTask.query";
import {DependencyList, DependencyListOnlyUseCase, StoreContract, Toto} from "@/primary/controller/chooseAndIgnoreTask";
import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";

class ChooseTaskSpy implements ChooseAndIgnoreTask.Contract {
    private _history: undefined | [number, number] = undefined;

    execute(chosenTaskId: number, ignoredTaskId: number): void {
        this._history = [chosenTaskId, ignoredTaskId];
    }

    history() {
        assert(this._history !== undefined, 'history() called before execute()');
        return this._history;
    }
}


class WhichTaskQueryForTest implements WhichTask.Contract {
    private _tasks: Task[] = [];

    query(): Task[] {
        return this._tasks;
    }

    feed(tasks: Task[]) {
        this._tasks = tasks;
    }
}

class StoreForTest {
    _history: any[] = [];

    history(): any[] {
        return this._history
    }

    dispatch(expectedElement: any) {
        this._history.push(expectedElement);
    }
}

describe('controller', () => {
    describe('inject use case', () => {
        class DependencyListForTest implements DependencyList {
            constructor(private readonly _chooseAndIgnoreTaskUseCase: ChooseAndIgnoreTask.Contract,
                        private readonly _store: StoreForTest,
                        private readonly _whichTaskQuery: WhichTask.Contract) {
            }

            whichTaskQuery(): WhichTask.Contract {
                return this._whichTaskQuery;
            }

            store() {
                return this._store;
            }

            chooseAndIgnoreTaskUseCase() {
                return this._chooseAndIgnoreTaskUseCase;
            }
        }

        it.each([
            [1, 2, [1, 2]],
            [2, 1, [2, 1]],
        ])
        ('should call chooseAndIgnoreTask with %p', (chosenTaskId, ignoredTaskId, expected) => {
            const spy = new ChooseTaskSpy();

            const controller = new Toto.Controller(new DependencyListForTest(spy, new StoreForTest(), new WhichTaskQueryForTest()));
            controller.chooseAndIgnoreTask(chosenTaskId, ignoredTaskId);

            expect(spy.history()).toEqual(expected);
        });

        it.each([
            [[], [WhichTaskUpdated({tasks: []})]],
            [[{id: 1, name: "buy the milk"}], [WhichTaskUpdated({tasks: [{id: 1, name: "buy the milk"}]})]],
            [[{id: 2, name: "buy the bread"}], [WhichTaskUpdated({tasks: [{id: 2, name: "buy the bread"}]})]],
            [[{id: 1, name: "buy the milk"}, {id: 2, name: "buy the bread"}], [WhichTaskUpdated({tasks: [{id: 1, name: "buy the milk"}, {id: 2, name: "buy the bread"}]})]],
        ])('should dispatch whichTaskUpdated', (tasks, expected) => {
            const whichTaskQuery = new WhichTaskQueryForTest();
            const store = new StoreForTest();
            whichTaskQuery.feed(tasks);

            const controller = new Toto.Controller(new DependencyListForTest(new ChooseTaskSpy(), store, whichTaskQuery));
            controller.chooseAndIgnoreTask(3, 4);

            // const expected = [WhichTaskUpdated({tasks: []})];
            expect(store.history()).toEqual(expected);
        });


    })

    describe('inject adapters', () => {
        class DependencyListForTest extends DependencyListOnlyUseCase {
            protected todolistForWhichTaskQuery(): WhichTask.Port.Todolist {
                return this._todolist2
            }

            constructor(private _todolist2: WhichTask.Port.Todolist, private readonly _todolist1: ChooseAndIgnoreTask.Port.Todolist, private readonly _store: StoreContract) {
                super();
            }

            store(): StoreContract {
                return this._store;
            }

            protected todolistForChooseAndIgnoreTaskUseCase(): ChooseAndIgnoreTask.Port.Todolist {
                return this._todolist1
            }

        }

        class SpyAdapter implements WhichTask.Port.Todolist, ChooseAndIgnoreTask.Port.Todolist {
            whichTask(): Task[] {
                return []
            }
            private _history: string[] = [];

            chooseAndIgnoreTask(_chosenTaskId: number, _ignoredTaskId: number): void {
                this._history.push('update todolist');
            }

            history() {
                return this._history;
            }
        }

        it('should update todolist and refresh tasks of screen', () => {
            const spy = new SpyAdapter();

            const controller = new Toto.Controller(new DependencyListForTest(spy, spy, new StoreForTest()));
            controller.chooseAndIgnoreTask(1, 2);

            expect(spy.history()).toEqual(["update todolist"]);
        })
    });


});