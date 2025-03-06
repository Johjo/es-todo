import type { DependenciesUseCase } from '../dependenciesUseCase.ts';
import { FetchTodolistPrimaryPort } from '../hexagon/fetchTodolist.usecase.ts';
import { OpenTaskPrimaryPort } from '../hexagon/openTask.usecase.ts';
import { AppDispatch } from '../hexagon/store.ts';

export class DependenciesUseCaseDummy implements DependenciesUseCase {
  fetchTodolist(_dispatch: AppDispatch): FetchTodolistPrimaryPort {
    throw new Error('Method not implemented.');
  }

  openTask(_dispatch: AppDispatch): OpenTaskPrimaryPort {
    throw new Error('Method not implemented.');
  }
}
