import {describe} from "vitest";
import {act, screen} from "@testing-library/react";
import {TaskCounter} from "@/app/components/TaskCounter";
import React from "react";
import {todoListFetched} from "@/lib/todolist.slice";
import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import {DependenciesList, TodolistReader} from "@/app/controller";


class EmptyDependencies implements DependenciesList {
    todolistReaderForRefreshTodolist(): TodolistReader {
        throw new Error("Method not implemented.");
    }
}

describe("TaskCounter", () => {
    it("should display 0 when load", () => {
        renderWithProvider(<TaskCounter/>, new EmptyDependencies());
        expect(screen.getByText('Il y a 0 tâche en cours')).toBeInTheDocument();
    });

    it.each([
        [0, 'Il y a 0 tâche en cours'],
        [1, 'Il y a 1 tâche en cours'],
        [10, 'Il y a 10 tâches en cours'],
    ])("should display the number of tasks when %s task(s)", (numberOfTasks, expected) => {
        const {store} = renderWithProvider(<TaskCounter/>, new EmptyDependencies());
        act(() => {
            store.dispatch(todoListFetched({numberOfTasks: numberOfTasks}));
        });

        expect(screen.getByText(expected)).toBeInTheDocument();
    });
});