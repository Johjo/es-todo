import {
  FromBackend,
  TodolistPageDisplayImpl,
  TodolistPageDisplayUseCase
} from '../../hexagon/todolistPageDisplay.usecase';
import { TodolistFetcherPort } from '../../hexagon/todolistPageDisplay.port';
import { AppStore, createStore } from '../../hexagon/store';

describe('Todolist page use case', () => {
  let sut: TodolistPageDisplayUseCase;
  let todolistFetcher: TodolistFetcherForTest;
  let store: AppStore;

  beforeEach(() => {
    store = createStore();
    todolistFetcher = new TodolistFetcherForTest();
    sut = new TodolistPageDisplayImpl(todolistFetcher, store);
  });

  it('should do nothing', () => {
    expect(store.getState().todolistPage).toEqual({ statut: 'idle' });
  });


  it('should indicate when loading started (no wait for async method)', () => {
    sut.execute();
    expect(store.getState().todolistPage).toEqual({ statut: 'loading' });
  });

  it('should indicate empty todolist when no task', async () => {
    todolistFetcher.feed({ tasks: [] });
    await sut.execute();

    expect(store.getState().todolistPage).toEqual({ statut: 'empty' });

  });

  it('should display todolist when one task', async () => {
    todolistFetcher.feed({ tasks: [{ key: '1', name: 'buy the milk' }] });

    await sut.execute();

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

    await sut.execute();
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


