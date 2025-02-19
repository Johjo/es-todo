import { createContext, useContext } from 'react';
import type { DependenciesUseCase } from './dependenciesUseCase.ts';

export const DependenciesContext = createContext<DependenciesUseCase | null>(null);

export function useDependenciesUseCase() {
  const context = useContext(DependenciesContext);
  if (context === null) {
    throw new Error('use case dependencies is not available');
  }
  return context;
}
