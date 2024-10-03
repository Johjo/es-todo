import {WhichTaskUpdated} from "@/lib/todolist.slice";
import {createContext, useContext} from "react";
import React from "react";

export type Task = {
    id: number
    ;
    name: string;
}

export type WhichTaskResponse = { tasks: Task[] };

export interface WhichTaskQuery {
    whichTask(): Promise<WhichTaskResponse>;
}

export interface DependenciesList {
    todolistReaderForRefreshTodolist(): WhichTaskQuery;
}

const DependenciesContext = createContext<DependenciesList | undefined>(undefined)

export const useDependencies = () => {
    const context = useContext(DependenciesContext);
    if (!context) {
        throw new Error("useDependencies doit être utilisé dans un DependenciesProvider");
    }
    return context;
};

export const DependenciesProvider: React.FC<{ dependencies: DependenciesList; children: React.ReactNode }> = ({
                                                                                                                  dependencies,
                                                                                                                  children,
                                                                                                              }) => {
    return <DependenciesContext.Provider value={dependencies}>{children}</DependenciesContext.Provider>;
};

export class Controller {
    constructor(private readonly store: any, private readonly dependencies: DependenciesList) {
    }

    askForWhichTask() {
        const allTodolist = this.dependencies.todolistReaderForRefreshTodolist();

        allTodolist.whichTask().then(whichTaskResponse => {
            this.store.dispatch(WhichTaskUpdated({tasks: whichTaskResponse.tasks}));
        });

    }
}