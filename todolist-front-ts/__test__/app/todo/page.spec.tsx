import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import TodolistPage from "@/app/todo/page";
import {describe} from "vitest";
import React from "react";
import {act, screen} from "@testing-library/react";
import {DependenciesList, WhichTaskQuery, WhichTaskResponse} from "@/app/controller";
import {WhichTask} from "@/lib/todolist.slice";


class SimpleWhichTaskQuery implements WhichTaskQuery {
    private whichTaskResponse: WhichTask | undefined;
    feed(whichTaskResponse: WhichTask) {
        this.whichTaskResponse = whichTaskResponse;
    }

    whichTask(): Promise<WhichTaskResponse> {
        if (!this.whichTaskResponse) {
            throw new Error("WhichTask has not been fed yet.");
        }

        return Promise.resolve(this.whichTaskResponse);
    }

}


describe("WhichTask", () => {
    it("should refresh which task when load page", async () => {
        const allTodolist = new SimpleWhichTaskQuery();
        const whichTaskResponse : WhichTask = {tasks: [{id: 1, name: 'Buy the milk'}]};
        allTodolist.feed(whichTaskResponse);

        const dependencies : DependenciesList = {
            todolistReaderForRefreshTodolist() {
                return allTodolist;
            }
        };

        const expectedText = 'Buy the milk';

        renderWithProvider(<TodolistPage/>, dependencies);
        await act(async () => {

        });


        expect(screen.getByText(expectedText)).toBeInTheDocument();
    });
});