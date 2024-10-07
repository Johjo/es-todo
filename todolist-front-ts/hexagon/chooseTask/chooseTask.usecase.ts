export class ChooseAndIgnoreTaskUseCase implements ChooseAndIgnoreTaskContract {
    private todolist: TodolistPort;

    constructor(adapters: { todolist: TodolistPort } | undefined) {
        assert(adapters?.todolist !== undefined, 'todolist called before injecting port');
        this.todolist = adapters.todolist;
    }

    execute(chosenTaskId: number, ignoredTaskId: number) {
        this.todolist.chooseAndIgnoreTask(chosenTaskId, ignoredTaskId)
    }
}

export interface ChooseAndIgnoreTaskContract {
    execute(chosenTaskId: number, ignoredTaskId: number): void;
}

export interface TodolistPort {
    chooseAndIgnoreTask(chosenTaskId: number, ignoredTaskId: number): void;
}


export namespace ChooseAndIgnoreTask {
    export const UseCase = ChooseAndIgnoreTaskUseCase;
    export type Contract = ChooseAndIgnoreTaskContract;

    export namespace Port {
        export type Todolist = TodolistPort;
        export type Builder = {
            todolist: (...args: any[]) => Port.Todolist;
        };
    }


    export function build(adapter: Port.Builder): ChooseAndIgnoreTask.Contract {
        assert(adapter?.todolist !== undefined, 'todolist called before injecting adapter');
        let todolist = adapter.todolist();
        return new UseCase({todolist})
    }
}