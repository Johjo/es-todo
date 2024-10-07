import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";
import {WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";
import {injectAllAdapter} from "@/primary/controller/injectAllAdapter";

type Builder<T> = (...args: any[]) => T;

export type Dependencies = WhichTask.Dependencies & ChooseAndIgnoreTask.Dependencies;

// Todo : faire un empty DependenciesAdapter pour les tests et passer une fonction qui fail forcément (pour remplacer les asserts)


export function injectDependencies(): Dependencies {
    return injectAllUseCase(injectAllAdapter());
}

export function injectAllUseCase(dependencies: Dependencies): Dependencies {
    return {}
}

function throwNotInjected(message: string) {
    return function (...args: any[]): any {
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


