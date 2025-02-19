import type { TodolistPageDisplayUseCase } from '../../../../../hexagon/todolistPageDisplay.usecase.ts';
import { DependenciesUseCase } from '../../../../../main/webapp/todolist/primary/dependenciesUseCase.ts';

export class DependenciesUseCaseDummy implements DependenciesUseCase {
  todolistPageDisplay(): TodolistPageDisplayUseCase {
    throw new Error('Method not implemented.');
  }

}
