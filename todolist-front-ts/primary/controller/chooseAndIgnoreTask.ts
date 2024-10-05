import {WhichTaskUpdated} from "@/lib/todolist.slice";
import {Dependencies} from "@/primary/controller/dependencies";
import {WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";
import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";

export class Controller {
    private _store: StoreContract;
    private _whichTaskQuery: WhichTask.Contract;
    private _chooseAndIgnoreTask: ChooseAndIgnoreTask.Contract;

    constructor(private readonly dependencies: Dependencies) {
        assert(this.dependencies?.chooseAndIgnoreTask?.useCase !== undefined, 'chooseAndIgnoreTask called before injecting use case');
        assert(this.dependencies?.store !== undefined, 'store called before injecting use case');
        assert(this.dependencies?.whichTask?.useCase !== undefined, 'whichTask called before injecting use case');

        this._chooseAndIgnoreTask = this.dependencies.chooseAndIgnoreTask.useCase;
        this._store = this.dependencies.store;
        this._whichTaskQuery = this.dependencies.whichTask?.useCase;
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
