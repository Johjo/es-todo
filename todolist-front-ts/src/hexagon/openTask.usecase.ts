import { TodolistUpdaterPort, UuidGeneratorPort } from './openTask.port';
import { AppDispatch } from './store';
import { taskOpened } from './todolistPage.slice';
import { DependenciesUseCase } from '../dependenciesUseCase.ts';

export interface OpenTaskContract {
  execute(dispatch: AppDispatch, taskName: string): Promise<void>;
}

export class OpenTaskUseCase implements OpenTaskContract {
  constructor(private readonly uuidGenerator: UuidGeneratorPort, private readonly todolistUpdater: TodolistUpdaterPort) {
  }

  async execute(dispatch: AppDispatch, taskName: string) {
    const taskKey = this.uuidGenerator.generate();
    await this.todolistUpdater.openTask('b69785c5-9266-486c-9655-52d85ad25bd5', { key: taskKey, name: taskName });
    dispatch(taskOpened({ key: taskKey, name: taskName }));
  }
}

export const openTask = (taskName: string) => async (dispatch: any, _getState: any, usesCases: DependenciesUseCase) => {
  const openTask = usesCases.openTask();
  await openTask.execute(dispatch, taskName);
};
