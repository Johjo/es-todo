import type { OpenTaskContract } from 'src/hexagon/openTask.usecase.ts';
import type { TodolistPageDisplayUseCase } from '../../../../../hexagon/todolistPageDisplay.usecase.ts';
import type { DependenciesUseCase } from '../../../../../main/webapp/todolist/primary/dependenciesUseCase.ts';

export class DependenciesUseCaseDummy implements DependenciesUseCase {
  openTask(): OpenTaskContract {
      throw new Error('Method not implemented.');
  }

  todolistPageDisplay(): TodolistPageDisplayUseCase {
    throw new Error('Method not implemented.');
  }

}
