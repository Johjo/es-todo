import {describe} from "vitest";
import {act, screen} from "@testing-library/react";
import React from "react";
import {todoListFetched} from "@/lib/todolist.slice";
import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import {aTodolist, EmptyDependencies} from "@/__test__/fixture";
import {FvpSession} from "@/app/components/FvpSession";


describe("FvpSession", () => {
    it("should display Nothing when no task", () => {
        renderWithProvider(<FvpSession/>, new EmptyDependencies());
        expect(screen.getByText('Rien à faire')).toBeInTheDocument();
    });

    it("should display the task when one task", () => {
        const {store} = renderWithProvider(<FvpSession/>, new EmptyDependencies());
        act(() => {
            store.dispatch(todoListFetched({...aTodolist(), tasks: [{id: "1", name: 'Faire la tâche'}]}));
        });
        expect(screen.getByText('Faire la tâche')).toBeInTheDocument();
    });

    it("should propose to choose the task when two tasks", () => {
        const {store} = renderWithProvider(<FvpSession/>, new EmptyDependencies());
        act(() => {
            store.dispatch(todoListFetched({
                ...aTodolist(),
                tasks: [{id: "1", name: 'Faire la tâche 1'}, {id: "2", name: 'Faire la tâche 2'}]
            }));
        });
        expect(screen.getByText('Faire la tâche 1')).toBeInTheDocument();
        expect(screen.getByText('Faire la tâche 2')).toBeInTheDocument();
    });

});