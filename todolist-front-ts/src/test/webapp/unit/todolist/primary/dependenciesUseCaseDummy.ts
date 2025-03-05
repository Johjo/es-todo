import type { OpenTaskContract } from 'src/hexagon/openTask.usecase.ts';
import type { FetchTodolistContract } from '../../../../../hexagon/fetchTodolist.usecase.ts';
import type { DependenciesUseCase } from '../../../../../dependenciesUseCase.ts';

export class DependenciesUseCaseDummy implements DependenciesUseCase {
  openTask(): OpenTaskContract {
      throw new Error('Method not implemented.');
  }

  fetchTodolist(): FetchTodolistContract {
    throw new Error('Method not implemented.');
  }

}
