import {Todolist} from "@/lib/todolist.slice";
import {DependenciesList, TodolistReader} from "@/app/controller";

export function aTodolist(): Todolist {
    return {numberOfTasks: 0, contexts: [], tasks: []};
}

export class EmptyDependencies implements DependenciesList {
    todolistReaderForRefreshTodolist(): TodolistReader {
        throw new Error("Method not implemented.");
    }
}