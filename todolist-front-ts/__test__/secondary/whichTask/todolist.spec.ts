import {injectAllAdapter} from "@/primary/controller/injectAllAdapter";

describe("Todolist", () => {
    it.skip("should return the list of tasks", async () => {
        const dependencies = injectAllAdapter()
        const sut = dependencies.whichTask?.adapter?.todolist()!
        const tasks = await sut.whichTask();
        expect(tasks).toMatchSnapshot();
    });
});