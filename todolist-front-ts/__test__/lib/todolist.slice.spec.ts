import {reducer, Todolist, todoListFetched} from "@/lib/todolist.slice"
import {aTodolist} from "@/__test__/fixture";
import {at} from "vitest/dist/chunks/reporters.WnPwkmgA";


describe("todolist reducer", () => {
    test("should return the initial state", () => {
        const expectedState: Todolist = aTodolist();
        expect(reducer(undefined, {type: 'unknown'})).toEqual(expectedState);
    });

    test("should fetch data", () => {
        const initialState: Todolist = aTodolist();
        const expectedState: Todolist = {...aTodolist(), numberOfTasks: 5};
        expect(reducer(initialState, todoListFetched({
            numberOfTasks: expectedState.numberOfTasks,
            tasks: expectedState.tasks,
            contexts: expectedState.contexts
        }))).toEqual(expectedState);
    });
});

