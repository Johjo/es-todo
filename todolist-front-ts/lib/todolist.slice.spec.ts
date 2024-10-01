import {reducer, Todolist, todoListFetched} from "@/lib/todolist.slice"



describe("todolist reducer", () => {
    test("should return the initial state", () => {
        const expectedState: Todolist = {numberOfTasks: 0};
        expect(reducer(undefined, {type: 'unknown'})).toEqual(expectedState);
    });

    test("should fetch data", () => {
        const initialState: Todolist = {numberOfTasks: 0};
        const expectedState: Todolist = {numberOfTasks: 5};
        expect(reducer(initialState, todoListFetched({numberOfTasks: 5}))).toEqual(expectedState);
    });
});

