import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import TodolistPage from "@/app/todo/page";
import {describe} from "vitest";
import React from "react";
import {act, screen} from "@testing-library/react";
import {Task, WhichTask} from "@/hexagon/whichTaskQuery/whichTask.query";
import {Dependencies, emptyDependencies} from "@/primary/controller/dependencies";

class WhichTaskQueryForTest implements WhichTask.Contract {
    private _tasks: Task[] | undefined;

    query(): Promise<Task[]> {
        assert(this._tasks !== undefined, 'WhichTask has not been feeded yet');
        return Promise.resolve(this._tasks);
    }

    feed(tasks: Task[]) {
        this._tasks = tasks;
    }
}

describe("WhichTask", () => {
    it("should refresh which task when load page", async () => {
        const whichTask = new WhichTaskQueryForTest();
        const expectedTask = {id: 1, name: 'Buy the milk'};
        whichTask.feed([expectedTask]);
        const dependencies: Dependencies = {
            ...emptyDependencies,
            whichTask: {...emptyDependencies.whichTask, useCase: () => whichTask},
        };

        await act(() => {
           renderWithProvider(<TodolistPage/>, dependencies);
        })
        expect(screen.getByText(expectedTask.name)).toBeInTheDocument();
    });
});