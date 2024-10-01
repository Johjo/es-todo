import React from "react";
import {makeStore} from "@/lib/store";
import {render} from "@testing-library/react";
import {Provider} from "react-redux";
import {DependenciesList, DependenciesProvider} from "@/app/controller";

export function renderWithProvider(ui: React.JSX.Element, dependencies: DependenciesList) {
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