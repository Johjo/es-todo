import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";

import React from "react";
import {act, screen} from "@testing-library/react";
import {todoListFetched} from "@/lib/todolist.slice";
import {Context} from "@/app/components/Context";
import {aTodolist} from "@/__test__/fixture";

describe("Context", () => {
    it("should display context", () => {

        const {store} = renderWithProvider(<Context/>, undefined);

        act(() => {
            store.dispatch(todoListFetched({...aTodolist(), contexts: ['#Contexte A', '#Contexte B']}));
        })

        expect(screen.getByText('Inbox')).toBeInTheDocument();
        expect(screen.getByText('#Contexte A')).toBeInTheDocument();
        expect(screen.getByText('#Contexte B')).toBeInTheDocument();
        expect(screen.getByText('All')).toBeInTheDocument();
    });
});