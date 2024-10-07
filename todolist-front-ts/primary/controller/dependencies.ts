import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";
import {WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";

type Builder<T> = (...args: any[]) => T;

export type Dependencies = Partial<{
    whichTask : Partial<{
        query: Builder<WhichTask.Contract>,
        adapter: {todolist: Builder<WhichTask.Port.Todolist>},
    }>;
    chooseAndIgnoreTask: Partial<{
        useCase: Builder<ChooseAndIgnoreTask.Contract>,
        adapter: { todolist: Builder<ChooseAndIgnoreTask.Port.Todolist>; },
    }>;
}>