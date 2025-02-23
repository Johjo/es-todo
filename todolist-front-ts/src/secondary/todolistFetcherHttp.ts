import { TodolistFetcherPort } from '../hexagon/todolistPageDisplay.port';
import { FromBackend } from '../hexagon/todolistPageDisplay.usecase';

export class TodolistFetcherHttp implements TodolistFetcherPort {
  constructor(private readonly url: string) {

  }
  async getTodolist(todolistKey: string): Promise<FromBackend.Todolist> {
    const response = await fetch(`${this.url}/todolist/${todolistKey}/task`, {
      method: 'GET',
      headers: {
        "Access-Control-Allow-Origin": "*"

  }
    });
    const todolist = await response.json() as FromBackend.Todolist;
    if (todolist.tasks.length === 0) {
      return { tasks: [] };
    }

    return {
      tasks: todolist.tasks.map(taskBackEnd => {
        return {key: taskBackEnd.key, name: taskBackEnd.name};
      })
    };

  }
}
