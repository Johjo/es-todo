import {describe} from "vitest";
import {act, screen} from "@testing-library/react";
import React from "react";
import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import {WhichTask} from "@/app/components/WhichTask";
import {WhichTaskFetched} from "@/lib/todolistPage.slice";
import {v4} from "uuid";


describe("WhichTask", () => {
    it("should display loading", () => {
        renderWithProvider(<WhichTask/>);
        expect(screen.getByText('Chargement des tâches...')).toBeInTheDocument();
    });

    it("should display nothing to do when no task", () => {
        const {store} = renderWithProvider(<WhichTask/>);
        act(() => {
            store.dispatch(WhichTaskFetched({tasks: []}));
        });
        expect(screen.getByText('Rien à faire')).toBeInTheDocument();
    });

    it("should display the task when one task", () => {
        const {store} = renderWithProvider(<WhichTask/>);
        act(() => {
            store.dispatch(WhichTaskFetched({tasks: [{key: v4(), name: 'Buy the milk'}]}));
        });
        expect(screen.getByText('Buy the milk')).toBeInTheDocument();
    });

    it("should propose to choose the task when two tasks", () => {
        const {store} = renderWithProvider(<WhichTask/>);
        act(() => {
            store.dispatch(WhichTaskFetched({
                tasks: [
                    {key: v4(), name: 'Buy the milk'},
                    {key: v4(), name: 'Buy the water'}
                ]
            }));
        });
        expect(screen.getByText('Buy the milk')).toBeInTheDocument();
        expect(screen.getByText('Buy the water')).toBeInTheDocument();
    });

    it("should propose to choose the task when many tasks", () => {
        const {store} = renderWithProvider(<WhichTask/>);
        act(() => {
            store.dispatch(WhichTaskFetched({
                tasks: [
                    {key: v4(), name: 'Buy the milk'},
                    {key: v4(), name: 'Buy the water'},
                    {key: v4(), name: 'Buy the eggs'},
                ]
            }));
        });
        expect(screen.getByText('Buy the milk')).toBeInTheDocument();
        expect(screen.getByText('Buy the water')).toBeInTheDocument();
    });

});