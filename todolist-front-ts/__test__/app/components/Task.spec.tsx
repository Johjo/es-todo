import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import React from "react";
import {screen} from "@testing-library/react";
import {Task} from "@/app/components/Task";
import {EmptyDependencies} from "@/__test__/fixture";

describe("Context", () => {
    it("should display context", () => {
        renderWithProvider(<Task key="1" name="The task"/>, new EmptyDependencies());


        expect(screen.getByText('The task')).toBeInTheDocument();
    });
});