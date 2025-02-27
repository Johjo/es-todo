import type { TodolistPageDisplayUseCase } from '../../../../hexagon/todolistPageDisplay.usecase.ts';
import type { OpenTaskContract } from '../../../../hexagon/openTask.usecase.ts';

export interface DependenciesUseCase {
  todolistPageDisplay(): TodolistPageDisplayUseCase;
  openTask(): OpenTaskContract;
}
