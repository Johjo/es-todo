import {WhichTaskUpdated} from "@/lib/todolist.slice";
import {Dependencies, DependenciesUseCase} from "@/primary/controller/dependencies";
import {WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";
import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";

export class Controller {
    private _store: StoreContract;
    private _whichTaskQuery: WhichTask.Contract;
    private _chooseAndIgnoreTask: ChooseAndIgnoreTask.Contract;

    constructor(dependencies: Dependencies, store: StoreContract) {
        this._store = store;
        this._whichTaskQuery = dependencies.whichTask.useCase(dependencies);
        this._chooseAndIgnoreTask = dependencies.chooseAndIgnoreTask.useCase(dependencies);
    }

    chooseAndIgnoreTask(chosenTaskId: number, ignoredTaskId: number) {
        this._chooseAndIgnoreTask.execute(chosenTaskId, ignoredTaskId);
        this._store.dispatch(WhichTaskUpdated({tasks: this._whichTaskQuery.query()}));
    }

    refreshWhichTask() {

    }
}

export interface StoreContract {
    dispatch(whichTaskUpdated: any): void;
}
