import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";
import {WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";
import {build} from "@/secondary/whichTask/todolistFromApi";

export type Dependencies = WhichTask.Dependencies & ChooseAndIgnoreTask.Dependencies;

function throwNotInjected(message: string) {
    return function (): any {
        throw new Error(message);
    };
}

export const emptyDependencies: Dependencies = {
    chooseAndIgnoreTask: {
        useCase: throwNotInjected("chooseAndIgnoreTask.useCase not injected"),
        adapter: {todolist: throwNotInjected("chooseAndIgnoreTask.adapter.todolist not Injected")},
    }, whichTask: {
        useCase: throwNotInjected(("whichTask.useCase not injected")),
        adapter: {todolist: throwNotInjected("whichTask.adapter.todolist not Injected")},
    }
}

export const allUseCasesDependencies: Dependencies = {
    ...emptyDependencies,
    chooseAndIgnoreTask: {...emptyDependencies.chooseAndIgnoreTask, useCase: ChooseAndIgnoreTask.build},
    whichTask: {...emptyDependencies.whichTask, useCase: WhichTask.build}
}

export const allAdaptersDependencies: Dependencies = {
    ...allUseCasesDependencies,
    whichTask: {...allUseCasesDependencies.whichTask, adapter: {todolist: build}}
}




