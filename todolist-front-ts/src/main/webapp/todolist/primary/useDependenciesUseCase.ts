import { createContext, useContext } from 'react';
import { TodolistPageDisplayUseCase } from '../../../../hexagon/todolistPageDisplay.usecase.ts';

export type UseCaseDependencies = {
  todolistPageDisplay: TodolistPageDisplayUseCase;
}
export const DependenciesContext = createContext<UseCaseDependencies | null>(null);

export function useDependenciesUseCase() {
  const context = useContext(DependenciesContext);
  if (context === null) {
    throw new Error('use case dependencies is not available');
  }
  return context;
}
