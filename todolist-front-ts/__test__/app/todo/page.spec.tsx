import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import TodolistPage from "@/app/todo/page";
import {describe} from "vitest";
import React from "react";
import {act, screen} from "@testing-library/react";
import {DependenciesList, Todolist, TodolistReader} from "@/app/controller";
import {aTodolist} from "@/__test__/fixture";


class SimpleTodolistReader implements TodolistReader {
    private todolist: Todolist | undefined;

    feed(todolist: Todolist) {
        this.todolist = todolist;
    }

    async onlyOne() {
        if (!this.todolist) {
            throw new Error("Todolist has not been fed yet.");
        }

        return this.todolist;
    }
}


describe("Todolist", () => {
    it("should refresh data when load page", async () => {
        const allTodolist = new SimpleTodolistReader();
        const externalTodolist : Todolist = {...aTodolist(), numberOfTasks: 2};
        allTodolist.feed(externalTodolist);

        const dependencies : DependenciesList = {
            todolistReaderForRefreshTodolist() {
                return allTodolist;
            }
        };

        const expectedText = 'Il y a 2 tâches en cours';

        renderWithProvider(<TodolistPage/>, dependencies);
        await act(async () => {

        });


        expect(screen.getByText(expectedText)).toBeInTheDocument();
    });
});