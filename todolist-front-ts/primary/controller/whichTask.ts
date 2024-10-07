import {WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";
import {StoreContract} from "@/primary/controller/chooseAndIgnoreTask";
import {Dependencies} from "@/primary/controller/dependencies";
import {WhichTaskUpdated} from "@/lib/todolist.slice";

export class Controller {
    private _whichTaskQuery: WhichTask.Contract;
    private _store: StoreContract;

    constructor(dependencies: Dependencies) {
        assert(dependencies.whichTask?.query !== undefined, 'whichTask query called before injecting use case');
        assert(dependencies.store !== undefined, 'store called before injecting use case');

        this._store = dependencies.store;
        this._whichTaskQuery = dependencies.whichTask.query();
    }


    execute() {
        const tasksToExamine = this._whichTaskQuery.query();

        this._store.dispatch(WhichTaskUpdated({
            tasks: tasksToExamine
        }));
    }

}