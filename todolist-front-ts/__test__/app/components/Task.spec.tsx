import {renderWithProvider} from "@/__test__/app/utils/renderWithProvider";
import {EmptyDependencies} from "@/__test__/app/components/fixture";
import React from "react";
import {screen} from "@testing-library/react";
import {Context} from "@/app/components/Context";
import {Task} from "@/app/components/Task";

describe("Context", () => {
    it("should display context", () => {
        renderWithProvider(<Task key="1" name="The task"/>, new EmptyDependencies());


        expect(screen.getByText('The task')).toBeInTheDocument();
    });
});