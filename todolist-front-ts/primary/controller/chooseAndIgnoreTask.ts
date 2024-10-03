
import {WhichTaskUpdated} from "@/lib/todolist.slice";
import {WhichTask} from "@/hexagon/whichTask.query";
import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask.usecase";

export namespace Toto {
    export class Controller {
        constructor(private readonly dependencies: DependencyList) {

        }

        chooseAndIgnoreTask(chosenTaskId: number, ignoredTaskId: number) {
            const chooseAndIgnoreTask = this.dependencies.chooseAndIgnoreTaskUseCase();
            chooseAndIgnoreTask.execute(chosenTaskId, ignoredTaskId);

            const store = this.dependencies.store()
            const whichTaskQuery = this.dependencies.whichTaskQuery();

            store.dispatch(WhichTaskUpdated({tasks: whichTaskQuery.query()}));
        }

        refreshWhichTask() {

        }
    }

}


export interface DependencyList {
    chooseAndIgnoreTaskUseCase(): ChooseAndIgnoreTask.Contract;

    whichTaskQuery(): WhichTask.Contract;

    store(): StoreContract;
}

export interface StoreContract {
    dispatch(whichTaskUpdated: any): void;
}
//
// export interface DependencyList {
//     useCase(): Contract;
//     port(): Port.DependencyList;
// }
//
// export interface DependencyList {
//     todolist(): Todolist;
// }
//


export abstract class DependencyListOnlyUseCase implements DependencyList {
    whichTaskQuery(): WhichTask.Contract {
        const todolist = this.todolistForWhichTaskQuery();
        return new WhichTask.Query(todolist);
    }

    chooseAndIgnoreTaskUseCase(): ChooseAndIgnoreTask.Contract {
        const todolist = this.todolistForChooseAndIgnoreTaskUseCase();
        return new ChooseAndIgnoreTask.UseCase(todolist);
    }


    abstract store(): StoreContract;

    protected abstract todolistForChooseAndIgnoreTaskUseCase(): ChooseAndIgnoreTask.Port.Todolist;

    protected abstract todolistForWhichTaskQuery(): WhichTask.Port.Todolist;
}