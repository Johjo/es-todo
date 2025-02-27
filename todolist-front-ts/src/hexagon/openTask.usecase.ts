import { TodolistUpdaterPort, UuidGeneratorPort } from './openTask.port';
import { AppDispatch, AppGetState, UseCases } from './store';
import { taskOpened } from './todolistPage.slice';

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

export const openTask = (taskName: string) => async (dispatch: AppDispatch, _getState: AppGetState, usesCases : UseCases) => {
  const { openTask }: { openTask: OpenTaskContract } = usesCases;
  await openTask.execute(dispatch, taskName);
};
