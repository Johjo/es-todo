import {AppStore} from "@/lib/store";
import {todoListFetched} from "@/lib/todolist.slice";
import {createContext, useContext} from "react";
import React from "react";

export type Todolist = { numberOfTasks: number };

export interface TodolistReader {
    onlyOne(): Promise<Todolist>;
}

export interface DependenciesList {
    todolistReaderForRefreshTodolist(): TodolistReader;
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

    refreshTodolist() {
        const allTodolist = this.dependencies.todolistReaderForRefreshTodolist();

        allTodolist.onlyOne().then(todolist => {
            this.store.dispatch(todoListFetched({numberOfTasks: todolist.numberOfTasks}));
        });

    }
}