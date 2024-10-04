export class ChooseAndIgnoreTaskUseCase implements ChooseAndIgnoreTaskContract {
    constructor(private readonly todolist: TodolistPort) {
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

