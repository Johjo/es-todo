import {DependenciesAdapter, DependenciesUseCase} from "@/primary/controller/dependencies";
import {build} from "@/secondary/whichTask/todolistFromApi";

export function injectAllAdapter(): DependenciesAdapter {
    return {whichTask: {adapter: {todolist: build}}};
}