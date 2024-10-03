export namespace WhichTask {
    export interface Contract {
        query(): Task[];
    }

    export class Query implements Contract {
        constructor(private readonly todolist: Port.Todolist) {

        }

        query(): Task[] {
            return this.todolist.whichTask();
        }
    }

    export type Task = {
        id: number;
        name: string;
    }

    export namespace Port {
        export interface Todolist {
            whichTask(): Task[];
        }

    }

}

export type Task = WhichTask.Task;