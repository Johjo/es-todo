import type { AppStore } from '../../../../../hexagon/store.ts';
import React from 'react';
import { render } from '@testing-library/react';
import { Provider } from 'react-redux';

export const renderWithDependencies = (store: AppStore) => (ui: React.ReactElement) => {
  return render(<Provider store={store}>
    {ui}
  </Provider>);
};
