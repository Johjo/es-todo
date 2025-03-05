import type { AppStore } from '../../../../../hexagon/store.ts';
import { DependenciesContext } from '../../../../../main/webapp/todolist/primary/useDependenciesUseCase.ts';
import React from 'react';
import { render } from '@testing-library/react';
import { Provider } from 'react-redux';
import type { DependenciesUseCase } from '../../../../../dependenciesUseCase.ts';

export const renderWithDependencies = (store: AppStore, useCaseDependencies: DependenciesUseCase) => (ui: React.ReactElement) => {
  return render(<DependenciesContext value={useCaseDependencies}>
    <Provider store={store}>
      {ui}
    </Provider>
  </DependenciesContext>);
};
