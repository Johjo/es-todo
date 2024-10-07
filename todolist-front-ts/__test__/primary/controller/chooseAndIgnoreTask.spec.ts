import {WhichTaskUpdated} from "@/lib/todolist.slice";
import {Controller} from "@/primary/controller/chooseAndIgnoreTask";
import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";
import {Task, WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";
import {
    allUseCasesDependencies,
    Dependencies,
    emptyDependencies,
    injectAllUseCase
} from "@/primary/controller/dependencies";
import {
    ChooseTaskForTest,
    StoreForTest,
    WhichTaskQueryForTest
} from "@/__test__/primary/controller/fixture";
import {adapter} from "next/dist/server/web/adapter";


describe('controller', () => {
    describe('inject use case', () => {
        it.each([
            [1, 2, [1, 2]],
            [2, 1, [2, 1]],
        ])
        ('should call chooseAndIgnoreTask with %p', (chosenTaskId, ignoredTaskId, expected) => {
            const chooseTask = new ChooseTaskForTest();
            const controller = new Controller({
                ...emptyDependencies,
                whichTask: {useCase: () => new WhichTaskQueryForTest()},
                chooseAndIgnoreTask: {useCase: () => chooseTask},
                // chooseAndIgnoreTask: {useCase: () => chooseTask},
                // whichTaskOld: {query: () => new WhichTaskQueryForTest()},
            }, new StoreForTest());

            controller.chooseAndIgnoreTask(chosenTaskId, ignoredTaskId);

            expect(chooseTask.history()).toEqual(expected);
        });

        it.each([
            [[], [WhichTaskUpdated({tasks: []})]],
            [[{id: 1, name: "buy the milk"}], [WhichTaskUpdated({tasks: [{id: 1, name: "buy the milk"}]})]],
            [[{id: 2, name: "buy the bread"}], [WhichTaskUpdated({tasks: [{id: 2, name: "buy the bread"}]})]],
            [[{id: 1, name: "buy the milk"}, {id: 2, name: "buy the bread"}], [WhichTaskUpdated({
                tasks: [{
                    id: 1,
                    name: "buy the milk"
                }, {id: 2, name: "buy the bread"}]
            })]],
        ])('should dispatch whichTaskUpdated', (tasks, expected) => {
            const whichTaskQuery = new WhichTaskQueryForTest();
            const store = new StoreForTest();
            whichTaskQuery.feed(tasks);

            const controller = new Controller({
                ...emptyDependencies,
                chooseAndIgnoreTask: {useCase: () => new ChooseTaskForTest()},
                whichTask: {useCase: () => whichTaskQuery}
            }, store);
            controller.chooseAndIgnoreTask(3, 4);

            expect(store.history()).toEqual(expected);
        });


    })

    describe('inject adapters', () => {
        class TodolistForTest implements WhichTask.Port.Todolist, ChooseAndIgnoreTask.Port.Todolist {
            private _tasks: Task[] | undefined = undefined;

            whichTask(): Task[] {
                assert(this._tasks !== undefined, 'whichTask() called before feed()');
                return this._tasks;
            }

            private _history: string[] = [];

            chooseAndIgnoreTask(_chosenTaskId: number, _ignoredTaskId: number): void {
                this._history.push('update todolist');
            }

            history() {
                return this._history;
            }

            feed(tasks: Task[]) {
                this._tasks = tasks;
            }
        }

        it('should update todolist and refresh tasks of screen', () => {
            const todolist = new TodolistForTest();
            const store = new StoreForTest();

            const expectedTask = {id: 5, name: "buy the milk"};
            todolist.feed([expectedTask]);

            const dependencies : Dependencies = {...allUseCasesDependencies,
                whichTask: {...allUseCasesDependencies.whichTask,adapter: {todolist: () => todolist}},
                chooseAndIgnoreTask: {...allUseCasesDependencies.chooseAndIgnoreTask, adapter: {todolist: () => todolist}}
            }

            const controller = new Controller(dependencies, store);
            controller.chooseAndIgnoreTask(1, 2);

            expect(todolist.history()).toEqual(["update todolist"]);
            expect(store.history()).toEqual([WhichTaskUpdated({tasks: [expectedTask]})]);
        })
    });


});