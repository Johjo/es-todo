import { DependenciesAdapter } from './dependencies.ts';
import type { TodolistFetcherPort } from './hexagon/fetchTodolist.port.ts';
import { TodolistFetcherHttp } from './secondary/todolistFetcherHttp.ts';
import type { OpenTaskUpdaterPort, UuidGeneratorPort } from './hexagon/openTask.port.ts';
import { UuidGeneratorRandom } from './secondary/uuidGeneratorRandom.ts';
import { TodolistUpdaterHttp } from './secondary/todolistUpdaterHttp.ts';

export class DependenciesAdapterForDemo implements DependenciesAdapter {
  todolistFetcher(): TodolistFetcherPort {
    return new TodolistFetcherHttp('https://todolist-ytreza-dev.osc-fr1.scalingo.io');
  }

  uuidGenerator(): UuidGeneratorPort {
    return new UuidGeneratorRandom();
  }

  todolistUpdater(): OpenTaskUpdaterPort {
    return new TodolistUpdaterHttp('https://todolist-ytreza-dev.osc-fr1.scalingo.io');
  }
}
