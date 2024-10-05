import {ChooseAndIgnoreTask} from "@/hexagon/chooseTask/chooseTask.usecase";
import {StoreContract} from "@/primary/controller/chooseAndIgnoreTask";
import {WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";

export type Dependencies = Partial<{
    store: StoreContract;
    chooseAndIgnoreTask: Partial<{ useCase: ChooseAndIgnoreTask.Contract, adapters: {todolist: ChooseAndIgnoreTask.Port.Todolist}}>
    whichTask: Partial<{ useCase: WhichTask.Contract, adapters: {todolist: WhichTask.Port.Todolist}}>;
}>