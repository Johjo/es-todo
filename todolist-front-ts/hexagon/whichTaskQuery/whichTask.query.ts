// Todo : stop to export

export interface WhichTaskContract {
    query(): Promise<Task[]>;
}

export interface TodolistPort {
    whichTask(): Promise<Task[]>;
}

export type Task = {
    id: number;
    name: string;
}

export class WhichTaskQuery implements WhichTaskContract {
    private todolist: TodolistPort;

    constructor(todolist: TodolistPort) {
        this.todolist = todolist;
    }

    async query(): Promise<Task[]> {
        return await this.todolist.whichTask();
    }
}


export namespace WhichTask {
    export type Contract = WhichTaskContract;
    export const Query = WhichTaskQuery;
    export namespace Port {
        export type Todolist = TodolistPort;
    }

    export type Dependencies = {
        whichTask: {
            useCase: (...args: any[]) => Contract,
            adapter: { todolist: (...args: any[]) => Port.Todolist; }
        }
    };

    export function build(dependencies: Dependencies): Contract {
        let todolist = dependencies.whichTask.adapter.todolist(dependencies)
        return new Query(todolist)
    }


}