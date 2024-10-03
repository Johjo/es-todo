import {WhichTask} from "@/hexagon/whichTask.query";


class TodolistForTest implements WhichTask.Port.Todolist {
    tasks: WhichTask.Task[] = [];

    feed(task: { name: string; id: number }) {
        this.tasks.push(task);
    }

    whichTask(): WhichTask.Task[] {
        return this.tasks;
    }
}

class ScreenForTest {
}

describe('updateWhichTask', () => {
    it('Should return nothing when no task', () => {
        const expected: WhichTask.Task[] = [];
        const sut = new WhichTask.Query(new TodolistForTest());
        const actual: WhichTask.Task[] = sut.query();
        expect(actual).toStrictEqual(expected);

    });

    it('Should return one task when only one task', () => {
        const expected: WhichTask.Task[] = [{id: 1, name: "buy the milk"}];
        const todolist = new TodolistForTest();
        todolist.feed(expected[0]);
        const sut = new WhichTask.Query(todolist);
        let actual: WhichTask.Task[] = sut.query();

        expect(actual).toStrictEqual(expected);
    });

    it('Can return two tasks', () => {
        const expected: WhichTask.Task[] = [{id: 1, name: "buy the milk"}, {id: 2, name: "buy the eggs"}];
        const todolist = new TodolistForTest();
        todolist.feed(expected[0]);
        todolist.feed(expected[1]);

        const sut = new WhichTask.Query(todolist);
        let actual: WhichTask.Task[] = sut.query();

        expect(actual).toStrictEqual(expected);
    })


});