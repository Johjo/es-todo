import {WhichTaskUpdated} from "@/lib/todolist.slice";
import {Dependencies} from "@/primary/controller/dependencies";
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

    async chooseAndIgnoreTask(chosenTaskId: number, ignoredTaskId: number) {
        await this._chooseAndIgnoreTask.execute(chosenTaskId, ignoredTaskId);
        const tasks = await this._whichTaskQuery.query();
        this._store.dispatch(WhichTaskUpdated({tasks: tasks}));
    }
}

export interface StoreContract {
    dispatch(whichTaskUpdated: any): void;
}
