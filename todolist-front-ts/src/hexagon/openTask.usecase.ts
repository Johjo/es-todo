import { OpenTaskUpdaterPort, UuidGeneratorPort } from './openTask.port';
import { AppDispatch, RootState } from './store';
import { taskOpened } from './todolistPage.slice';
import { DependenciesUseCase } from '../dependenciesUseCase.ts';
import { Action, ThunkAction } from '@reduxjs/toolkit';

export interface OpenTaskPrimaryPort {
  execute(taskName: string): Promise<void>;
}

export class OpenTaskUseCase implements OpenTaskPrimaryPort {
  constructor(private readonly uuidGenerator: UuidGeneratorPort, private readonly todolistUpdater: OpenTaskUpdaterPort, private readonly dispatch: AppDispatch) {
  }

  async execute(taskName: string): Promise<void> {
    const taskKey = this.uuidGenerator.generate();
    await this.todolistUpdater.openTask('b69785c5-9266-486c-9655-52d85ad25bd5', { key: taskKey, name: taskName });
    this.dispatch(taskOpened({ key: taskKey, name: taskName }));
  }
}

export const openTask = (taskName: string): ThunkAction<Promise<void>, RootState, DependenciesUseCase, Action> => async (dispatch: AppDispatch, _getState: any, useCase: DependenciesUseCase) => {
  await useCase.openTask(dispatch).execute(taskName);
};
