import {
  fetchTodolist,
  type FetchTodolistContract,
  FetchTodolistUseCase,
  FromBackend
} from '../../hexagon/fetchTodolist.usecase';
import { TodolistFetcherPort } from '../../hexagon/fetchTodolist.port';
import { AppStore, createAppStore } from '../../hexagon/store';
import { DependenciesUseCaseDummy } from '../webapp/unit/todolist/primary/dependenciesUseCaseDummy';

class DependenciesUseCaseForTest extends DependenciesUseCaseDummy {
  constructor(private readonly useCase: FetchTodolistUseCase) {
    super();
  }

  fetchTodolist(): FetchTodolistContract {
    return this.useCase;
  }
}

describe('fetch todolist use case', () => {
  let todolistFetcher: TodolistFetcherForTest;
  let store: AppStore;

  beforeEach(() => {
    todolistFetcher = new TodolistFetcherForTest();
    store = createAppStore(new DependenciesUseCaseForTest(new FetchTodolistUseCase(todolistFetcher)));
  });

  it('should do nothing', () => {
    expect(store.getState().todolistPage).toEqual({ statut: 'idle' });
  });


  it('should indicate when loading started (no wait for async method)', () => {
    store.dispatch(fetchTodolist());
    expect(store.getState().todolistPage).toEqual({ statut: 'loading' });
  });

  it('should indicate empty todolist when no task', async () => {
    todolistFetcher.feed({ tasks: [] });
    await store.dispatch(fetchTodolist());

    expect(store.getState().todolistPage).toEqual({ statut: 'empty' });

  });

  it('should display todolist when one task', async () => {
    todolistFetcher.feed({ tasks: [{ key: '1', name: 'buy the milk' }] });

    await store.dispatch(fetchTodolist());

    expect(store.getState().todolistPage).toEqual({
      statut: 'atLeastOneTask',
      tasks: [{ key: '1', name: 'buy the milk' }]
    });
  });

  it('should display todolist when many task', async () => {
    todolistFetcher.feed({
      tasks: [
        { key: '1', name: 'buy the milk' },
        { key: '2', name: 'buy the water' }]
    });

    await store.dispatch(fetchTodolist());
  });
});


class TodolistFetcherForTest implements TodolistFetcherPort {
  private _todolist: FromBackend.Todolist | undefined = undefined;

  feed(todolist: FromBackend.Todolist) {
    this._todolist = todolist;
  }

  async getTodolist() {
    while (this._todolist === undefined) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    return this._todolist;
  }
}


