import {Todolist} from "@/lib/todolist.slice";
import {DependenciesList, WhichTaskQuery} from "@/app/controller";

export function aTodolist(): Todolist {
    return {numberOfTasks: 0, contexts: [], tasks: []};
}

export class EmptyDependencies implements DependenciesList {
    todolistReaderForRefreshTodolist(): WhichTaskQuery {
        throw new Error("Method not implemented.");
    }
}