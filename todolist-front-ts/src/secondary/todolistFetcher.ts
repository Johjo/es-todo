import { TodolistFetcherPort } from '../hexagon/todolistPageDisplay.port';
import { FromBackend } from '../hexagon/todolistPageDisplay.usecase';

export class TodolistFetcher implements TodolistFetcherPort {
  async getTodolist(): Promise<FromBackend.Todolist> {
    return { tasks: [ { key: '1', name: 'task 1' }, { key: '2', name: 'task 2' } ] };
  }
}
