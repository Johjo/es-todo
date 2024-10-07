import {allAdaptersDependencies} from "@/primary/controller/dependencies";
import {TodolistFromApi} from "@/secondary/whichTask/todolistFromApi";

describe("Todolist", () => {
    it("should return the list of tasks", async () => {
        const sut : TodolistFromApi = allAdaptersDependencies.whichTask.adapter.todolist()
        const tasks = await sut.whichTask();
        expect(tasks).toMatchSnapshot();
    });
});