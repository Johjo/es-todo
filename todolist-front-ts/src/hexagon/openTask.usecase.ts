import { TodolistUpdaterPort, UuidGeneratorPort } from './openTask.port';
import { AppStore } from './store';
import { taskOpened } from './todolistPage.slice';

export interface OpenTaskContract {
  execute(taskName: string): Promise<void>;
}

export class OpenTaskUseCase implements OpenTaskContract {
  constructor(private readonly uuidGenerator: UuidGeneratorPort, private readonly todolistUpdater: TodolistUpdaterPort, private readonly store: AppStore) {
  }

  async execute(taskName: string) {
    const taskKey = this.uuidGenerator.generate();
    await this.todolistUpdater.openTask("b69785c5-9266-486c-9655-52d85ad25bd5", { key: taskKey, name: taskName });
    this.store.dispatch(taskOpened({ key: taskKey, name: taskName }));
  }
}

