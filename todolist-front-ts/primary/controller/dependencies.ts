import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";
import {StoreContract} from "@/primary/controller/chooseAndIgnoreTask";
import {WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";

type Builder<T> = (...args: any[]) => T;

export type Dependencies = Partial<{
    store: StoreContract;
    whichTask : Partial<{
        query: Builder<WhichTask.Contract>,
        adapter: {todolist: Builder<WhichTask.Port.Todolist>},
    }>;
    chooseAndIgnoreTask: Partial<{
        useCase: Builder<ChooseAndIgnoreTask.Contract>,
        adapter: { todolist: Builder<ChooseAndIgnoreTask.Port.Todolist>; },
    }>;
}>