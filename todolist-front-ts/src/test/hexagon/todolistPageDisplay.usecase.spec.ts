import { TodolistPresentation } from '../../hexagon/todolistPage.slice';
import {
  FromBackend,
  TodolistPageDisplayImpl,
  TodolistPageDisplayUseCase
} from '../../hexagon/todolistPageDisplay.usecase';
import { TodolistFetcherPort, TodolistPageDisplayStorePort } from '../../hexagon/todolistPageDisplay.port';

class TodolistPageDisplayStoreForTest implements TodolistPageDisplayStorePort {
  private _history: TodolistPresentation[] = [];

  history() {
    return this._history;
  }

  displayTodolistPage(presentation: TodolistPresentation) {
    this._history.push(presentation);
  }
}


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

describe('Todolist page use case', () => {
  let store: TodolistPageDisplayStoreForTest;
  let sut: TodolistPageDisplayUseCase;
  let todolistFetcher: TodolistFetcherForTest;

  beforeEach(() => {
    store = new TodolistPageDisplayStoreForTest();
    todolistFetcher = new TodolistFetcherForTest();
    sut = new TodolistPageDisplayImpl(store, todolistFetcher);
  });

  it('should do nothing', () => {
    expect(store.history()).toEqual([]);
  });


  it('should indicate when loading started (no wait for async method)', () => {
    sut.execute();

    expect(store.history()).toEqual<TodolistPresentation[]>([{ statut: 'loading' }]);
  });

  it('should indicate empty todolist when no task', async () => {
    todolistFetcher.feed({ tasks: [] });
    await sut.execute();

    expect(store.history()).toEqual<TodolistPresentation[]>([
      { statut: 'loading' },
      { statut: 'empty' }
    ]);
  });

  it('should display todolist when one task', async () => {
    todolistFetcher.feed({ tasks: [{ key: '1', name: 'buy the milk' }] });

    await sut.execute();

    expect(store.history()).toEqual<TodolistPresentation[]>([
      { statut: 'loading' },
      { statut: 'atLeastOneTask', tasks: [{ key: '1', name: 'buy the milk' }] }
    ]);
  });

  it('should display todolist when many task', async () => {
    todolistFetcher.feed({
      tasks: [
        { key: '1', name: 'buy the milk' },
        { key: '2', name: 'buy the water' }]
    });

    await sut.execute();

    expect(store.history()).toEqual<TodolistPresentation[]>([
      { statut: 'loading' },
      { statut: 'atLeastOneTask', tasks: [{ key: '1', name: 'buy the milk' }, { key: '2', name: 'buy the water' }] }
    ]);
  });
});

