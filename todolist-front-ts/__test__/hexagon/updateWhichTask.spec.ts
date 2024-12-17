import {Task, WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";

class TodolistForTest implements WhichTask.Port.Todolist {
    tasks: Task[] = [];

    feed(task: { name: string; id: number }) {
        this.tasks.push(task);
    }

    whichTask(): Promise<Task[]> {
        return Promise.resolve(this.tasks);
    }
}

describe('updateWhichTask', () => {
    it('Should return nothing when no task', async () => {
        const expected: Task[] = [];
        const sut = new WhichTask.Query(new TodolistForTest());
        const actual: Task[] = await sut.query();
        expect(actual).toStrictEqual(expected);

    });

    it('Should return one task when only one task', async () => {
        const expected: Task[] = [{key: 1, name: "buy the milk"}];
        const todolist = new TodolistForTest();
        todolist.feed(expected[0]);
        const sut = new WhichTask.Query(todolist);
        let actual: Task[] = await sut.query();

        expect(actual).toStrictEqual(expected);
    });

    it('Can return two tasks', async () => {
        const expected: Task[] = [{key: 1, name: "buy the milk"}, {key: 2, name: "buy the eggs"}];
        const todolist = new TodolistForTest();
        todolist.feed(expected[0]);
        todolist.feed(expected[1]);

        const sut = new WhichTask.Query(todolist);
        let actual: Task[] = await sut.query();

        expect(actual).toStrictEqual(expected);
    })


});