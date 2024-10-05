import {WhichTaskUpdated} from "@/lib/todolist.slice";
import {StoreForTest, WhichTaskQueryForTest} from "@/__test__/primary/controller/fixture";
import {Controller} from "@/primary/controller/whichTask";


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
        const dependencies = {whichTask: {useCase: whichTaskQuery}, store: store};
        new Controller(dependencies).execute();

        // assert
        expect(store.history()).toEqual([expected]);
    })
});