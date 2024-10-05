import {describe} from "vitest";
import {act, screen} from "@testing-library/react";
import React from "react";
import {todoListFetched, WhichTaskUpdated} from "@/lib/todolist.slice";
import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import {aTodolist} from "@/__test__/fixture";
import {WhichTask} from "@/app/components/WhichTask";


describe("WhichTask", () => {
    it("should display Nothing when no task", () => {
        renderWithProvider(<WhichTask/>, undefined);
        expect(screen.getByText('Rien à faire')).toBeInTheDocument();
    });

    it("should display the task when one task", () => {
        const {store} = renderWithProvider(<WhichTask/>, undefined);
        act(() => {
            store.dispatch(WhichTaskUpdated({tasks: [{id: 1, name: 'Faire la tâche'}]}));
        });
        expect(screen.getByText('Faire la tâche')).toBeInTheDocument();
    });

    it("should display the task when one task", () => {
        const {store} = renderWithProvider(<WhichTask/>, undefined);
        act(() => {
            store.dispatch(todoListFetched({...aTodolist(), tasks: [{id: 1, name: 'Faire la tâche'}]}));
        });
        expect(screen.getByText('Faire la tâche')).toBeInTheDocument();
    });

    it("should propose to choose the task when two tasks", () => {
        const {store} = renderWithProvider(<WhichTask/>, undefined);
        act(() => {
            store.dispatch(todoListFetched({
                ...aTodolist(),
                tasks: [{id: 1, name: 'Faire la tâche 1'}, {id: 2, name: 'Faire la tâche 2'}]
            }));
        });
        expect(screen.getByText('Faire la tâche 1')).toBeInTheDocument();
        expect(screen.getByText('Faire la tâche 2')).toBeInTheDocument();
    });

});