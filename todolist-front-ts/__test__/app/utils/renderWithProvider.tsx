import React from "react";
import {makeStore} from "@/lib/store";
import {render} from "@testing-library/react";
import {Provider} from "react-redux";
import {DependenciesProvider} from "@/app/dependenciesProvider";
import {Dependencies} from "@/primary/controller/dependencies";

export function renderWithProvider(ui: React.JSX.Element, dependencies: Dependencies) {

    const store = makeStore();
    return {
        ...render(
            <Provider store={store}>
                <DependenciesProvider dependencies={dependencies}>
                    {ui}
                </DependenciesProvider>
            </Provider>), store
    };
}