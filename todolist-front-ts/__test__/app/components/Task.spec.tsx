import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import React from "react";
import {screen} from "@testing-library/react";
import {Task} from "@/app/components/Task";

describe("Context", () => {
    it("should display context", () => {
        renderWithProvider(<Task key="1" name="The task"/>);


        expect(screen.getByText('The task')).toBeInTheDocument();
    });
});