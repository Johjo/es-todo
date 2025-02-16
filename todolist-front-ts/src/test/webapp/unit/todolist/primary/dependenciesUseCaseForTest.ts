import { UseCaseDependencies } from '../../../../../main/webapp/todolist/primary/useDependenciesUseCase.ts';
import { TodolistPageDisplayUseCase } from '../../../../../hexagon/todolistPageDisplay.usecase.ts';

class TodolistPageDisplayUseCaseDummy implements TodolistPageDisplayUseCase {
  execute(): Promise<void> {
    throw new Error('Method not implemented.');
  }
}

export function useCaseDependenciesForTest(): UseCaseDependencies {
  return { todolistPageDisplay: new TodolistPageDisplayUseCaseDummy() };
}
