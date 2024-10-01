import {reducer, Todolist, todoListFetched} from "@/lib/todolist.slice"



describe("todolist reducer", () => {
    test("should return the initial state", () => {
        const expectedState: Todolist = {numberOfTasks: 0, contexts: []};
        expect(reducer(undefined, {type: 'unknown'})).toEqual(expectedState);
    });

    test("should fetch data", () => {
        const initialState: Todolist = {numberOfTasks: 0, contexts: []};
        const expectedState: Todolist = {numberOfTasks: 5, contexts: []};
        expect(reducer(initialState, todoListFetched({numberOfTasks: 5, contexts: []}))).toEqual(expectedState);
    });
});

