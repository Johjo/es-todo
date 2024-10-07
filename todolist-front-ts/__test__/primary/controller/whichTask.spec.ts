import {WhichTaskUpdated} from "@/lib/todolist.slice";
import {StoreForTest, WhichTaskQueryForTest} from "@/__test__/primary/controller/fixture";
import {Controller} from "@/primary/controller/whichTask";
import {Dependencies, emptyDependencies} from "@/primary/controller/dependencies";


describe('controller', () => {
    it('should dispatch whichTaskUpdated', async () => {
        // arrange
        const expected = WhichTaskUpdated({
            tasks: [{
                id: 1,
                name: "buy the milk"
            }, {id: 2, name: "buy the bread"}]
        })
        const tasksToExamine = [{id: 1, name: "buy the milk"}, {id: 2, name: "buy the bread"}];
        const whichTaskQuery = new WhichTaskQueryForTest();
        const store = new StoreForTest();

        whichTaskQuery.feed(tasksToExamine);
        // act
        const dependencies: Dependencies = {
            ...emptyDependencies,
            whichTask: {...emptyDependencies.whichTask, useCase: () => whichTaskQuery}
        }

        const controller = new Controller(dependencies, store);
        await controller.execute();

        // assert
        expect(store.history()).toEqual([expected]);
    })
});