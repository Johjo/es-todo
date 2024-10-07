import {createContext, useContext} from "react";
import React from "react";
import {Dependencies} from "@/primary/controller/dependencies";
const DependenciesContext = createContext<Dependencies |  undefined>(undefined)

export const useDependencies = () => {
    const context = useContext(DependenciesContext);
    if (!context) {
        throw new Error("useDependencies doit être utilisé dans un DependenciesProvider");
    }
    return context;
};

export const DependenciesProvider: React.FC<{ dependencies: Dependencies | undefined; children: React.ReactNode }> = (
    {
        dependencies,
        children,
    }) => {
    return <DependenciesContext.Provider value={dependencies}>{children}</DependenciesContext.Provider>;
};
