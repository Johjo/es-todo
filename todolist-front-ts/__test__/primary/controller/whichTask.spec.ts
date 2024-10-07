import {WhichTaskUpdated} from "@/lib/todolist.slice";
import {StoreForTest, WhichTaskQueryForTest} from "@/__test__/primary/controller/fixture";
import {Controller} from "@/primary/controller/whichTask";
import {Dependencies, DependenciesUseCase, emptyDependencies} from "@/primary/controller/dependencies";


describe('controller', () => {
    it('should dispatch whichTaskUpdated', () => {
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

        new Controller(dependencies, store).execute();

        // assert
        expect(store.history()).toEqual([expected]);
    })
});