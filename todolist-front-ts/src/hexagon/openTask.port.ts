export interface TodolistUpdaterPort {
  openTask(todolistKey: string, task: ToBackend.Task): Promise<void>;
}

export interface UuidGeneratorPort {
  generate(): string;
}

export namespace ToBackend {
  export type Task = { key: string, name: string };
}
