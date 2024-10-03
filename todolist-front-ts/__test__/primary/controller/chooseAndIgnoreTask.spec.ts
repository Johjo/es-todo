import {ChooseAndIgnoreTaskContract, ScreenPort, TodolistPort} from "@/hexagon/chooseTask.usecase";
import {Controller, DependencyList, DependencyListOnlyUseCase} from "@/primary/controller";

class ChooseTaskSpy implements ChooseAndIgnoreTaskContract {
    private _history: undefined | [number, number] = undefined;

    execute(chosenTaskId: number, ignoredTaskId: number): void {
        this._history = [chosenTaskId, ignoredTaskId];
    }

    history() {
        assert(this._history !== undefined, 'history() called before execute()');
        return this._history;
    }
}


describe('controller', () => {
    describe('inject use case', () => {
        class DependencyListForTest implements DependencyList {
            constructor(private readonly _chooseAndIgnoreTaskUseCase: ChooseAndIgnoreTaskContract) {
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

            const controller = new Controller(new DependencyListForTest(spy));
            controller.askForWhichTask(chosenTaskId, ignoredTaskId);

            expect(spy.history()).toEqual(expected);
        });

    })

    describe('inject adapters', () => {
        class DependencyListForTest extends DependencyListOnlyUseCase {
            constructor(private readonly _todolist: TodolistPort, private readonly _screen: ScreenPort) {
                super();
            }

            protected todolistForChooseAndIgnoreTaskUseCase(): TodolistPort {
                return this._todolist
            }

            protected screenForChooseAndIgnoreTaskUseCase(): ScreenPort {
                return this._screen;
            }
        }

        class SpyAdapter implements TodolistPort, ScreenPort {
            private _history: string[] = [];

            refreshTasks(): void {
                this._history.push('refresh tasks of screen');
            }

            chooseAndIgnoreTask(chosenTaskId: number, ignoredTaskId: number): void {
                this._history.push('update todolist');
            }

            history() {
                return this._history;
            }
        }

        it('should update todolist and refresh tasks of screen', () => {
            const spy = new SpyAdapter();

            const controller = new Controller(new DependencyListForTest(spy, spy));
            controller.askForWhichTask(1, 2);

            expect(spy.history()).toEqual(["update todolist", "refresh tasks of screen"]);
        })
    });


});