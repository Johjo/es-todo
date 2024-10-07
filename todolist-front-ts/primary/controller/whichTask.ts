import {WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";
import {StoreContract} from "@/primary/controller/chooseAndIgnoreTask";
import {Dependencies} from "@/primary/controller/dependencies";
import {WhichTaskUpdated} from "@/lib/todolist.slice";

export class Controller {
    private _whichTaskQuery: WhichTask.Contract;
    private _store: StoreContract;

    constructor(dependencies: Dependencies, store: StoreContract) {
        this._store = store;
        this._whichTaskQuery = dependencies.whichTask.useCase(dependencies)
    }


    async execute() {
        const tasksToExamine = await this._whichTaskQuery.query();

        this._store.dispatch(WhichTaskUpdated({
            tasks: tasksToExamine
        }));
    }

}