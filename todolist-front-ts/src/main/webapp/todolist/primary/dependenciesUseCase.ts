import type { TodolistPageDisplayUseCase } from '../../../../hexagon/todolistPageDisplay.usecase.ts';

export interface DependenciesUseCase {
  todolistPageDisplay(): TodolistPageDisplayUseCase;
}
