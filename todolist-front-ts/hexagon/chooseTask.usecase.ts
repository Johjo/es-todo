
export class ChooseTaskUseCase implements ChooseAndIgnoreTaskContract {
    constructor(private readonly todolist: TodolistPort, private screen: ScreenPort) {

    }

    execute(chosenTaskId: number, ignoredTaskId: number) {
        this.todolist.chooseAndIgnoreTask(chosenTaskId, ignoredTaskId)
        this.screen.refreshTasks();
    }
}

export interface ChooseAndIgnoreTaskContract {
    execute(chosenTaskId: number, ignoredTaskId: number) : void;
}


export interface TodolistPort {
    chooseAndIgnoreTask(chosenTaskId: number, ignoredTaskId: number): void;
}

export interface ScreenPort {
    refreshTasks(): void;
}