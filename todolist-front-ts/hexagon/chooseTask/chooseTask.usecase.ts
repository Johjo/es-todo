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
    }
}