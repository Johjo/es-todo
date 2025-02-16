import type { AppStore } from '../../../../../hexagon/store.ts';
import {
  DependenciesContext,
  UseCaseDependencies
} from '../../../../../main/webapp/todolist/primary/useDependenciesUseCase.ts';
import React from 'react';
import { render } from '@testing-library/react';
import { Provider } from 'react-redux';

export const renderWithDependencies = (store: AppStore, useCaseDependencies: UseCaseDependencies) => (ui: React.ReactElement) => {
  return render(<DependenciesContext value={useCaseDependencies}>
    <Provider store={store}>
      {ui}
    </Provider>
  </DependenciesContext>);
};
