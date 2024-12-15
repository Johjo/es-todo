import {describe} from "vitest";
import {act, screen} from "@testing-library/react";
import {TaskCounter} from "@/app/components/TaskCounter";
import React from "react";
import {todoListFetched} from "@/lib/todolist.slice";
import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import {aTodolist} from "@/__test__/fixture";
import {WhichTask} from "@/app/components/WhichTask";
import {NumberOfTasksFetched} from "@/lib/todolistPage.slice";


describe("TaskCounter", () => {
    it("should display loading", () => {
        renderWithProvider(<TaskCounter/>);
        expect(screen.getByText('Il y a ? tâche(s) en cours (Chargement...)')).toBeInTheDocument();
    });

    it.each([
        [0, 'Il y a 0 tâche en cours'],
        [1, 'Il y a 1 tâche en cours'],
        [10, 'Il y a 10 tâches en cours'],
    ])("should display the number of tasks when %s task(s)", (numberOfTasks, expected) => {
        const {store} = renderWithProvider(<TaskCounter/>);
        act(() => {
            store.dispatch(NumberOfTasksFetched({numberOfTasks: numberOfTasks}));
        });

        expect(screen.getByText(expected)).toBeInTheDocument();
    });
});