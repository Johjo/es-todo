// Todo : stop to export
export interface WhichTaskContract {
    query(): Task[];
}

export interface TodolistPort {
    whichTask(): Task[];
}

export type Task = {
    id: number;
    name: string;
}

export class WhichTaskQuery implements WhichTaskContract {
    private todolist: TodolistPort;

    constructor(adapters: {todolist: TodolistPort} | undefined) {
        assert(adapters?.todolist !== undefined, 'todolist called before injecting adapters');
        this.todolist = adapters.todolist;
    }

    query(): Task[] {
        return this.todolist.whichTask();
    }
}




export namespace WhichTask {
    export type Contract = WhichTaskContract;
    export const Query = WhichTaskQuery;
    export namespace Port {
        export type Todolist = TodolistPort;
        export type Builder = {
            todolist: (...args: any[]) => Port.Todolist;
        }
    }

    export function build(adapter: Port.Builder): Contract {
        assert(adapter?.todolist !== undefined, 'todolist called before injecting adapter');
        let todolist = adapter.todolist();
        return new Query({todolist : todolist})
    }


}