import {ChooseAndIgnoreTaskContract, ChooseTaskUseCase, ScreenPort, TodolistPort} from "@/hexagon/chooseTask.usecase";

export class Controller {
    constructor(private readonly dependencies: DependencyList) {

    }

    askForWhichTask(chosenTaskId: number, ignoredTaskId: number) {
        const chooseAndIgnoreTask = this.dependencies.chooseAndIgnoreTaskUseCase();
        chooseAndIgnoreTask.execute(chosenTaskId, ignoredTaskId);
    }
}

export interface DependencyList {
    chooseAndIgnoreTaskUseCase(): ChooseAndIgnoreTaskContract;
}

export abstract class DependencyListOnlyUseCase implements DependencyList {
    chooseAndIgnoreTaskUseCase(): ChooseAndIgnoreTaskContract {
        const todolist = this.todolistForChooseAndIgnoreTaskUseCase();
        const screen = this.screenForChooseAndIgnoreTaskUseCase();
        return new ChooseTaskUseCase(todolist, screen);
    }

    protected abstract todolistForChooseAndIgnoreTaskUseCase(): TodolistPort;

    protected abstract screenForChooseAndIgnoreTaskUseCase(): ScreenPort;
}