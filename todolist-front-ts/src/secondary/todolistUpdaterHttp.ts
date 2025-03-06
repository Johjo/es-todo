import { ToBackend, OpenTaskUpdaterPort } from '../hexagon/openTask.port';

export class TodolistUpdaterHttp implements OpenTaskUpdaterPort {
  constructor(private readonly url: string) {
  }

  async openTask(todolistKey: string, task: ToBackend.Task): Promise<void> {
    const finalUrl = `${this.url}/todolist/${todolistKey}/task/${task.key}`;

    await fetch(finalUrl, {
      method: 'POST',
      headers: { 'content-type': 'application/json;charset=UTF-8' },
      body: JSON.stringify({ name: task.name })
    });
  }

}
