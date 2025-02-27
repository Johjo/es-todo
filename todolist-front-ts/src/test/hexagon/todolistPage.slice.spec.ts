import { v4 } from 'uuid';
import {
  emptyTodolistFetched,
  selectTodolistPage,
  todolistFetched,
  todolistFetchingStarted
} from '../../hexagon/todolistPage.slice';
import { AppStore, createStore } from '../../hexagon/store';


describe('Todolist', () => {
  let store: AppStore;
  beforeEach(() => {
    store = createStore();
  });

  it('initial state should be idle', () => {
    expect(selectTodolistPage(store.getState())).toEqual({ statut: 'idle' });
  });

  it('should load todolist', () => {
    store.dispatch(todolistFetchingStarted());
    expect(selectTodolistPage(store.getState())).toEqual({ statut: 'loading' });
  });


  it('should fetch empty todolist', () => {
    store.dispatch(emptyTodolistFetched());

    expect(selectTodolistPage(store.getState())).toEqual({ statut: 'empty' });
  });

  it('should fetch at least one task', () => {
    const task_one = { key: v4(), name: 'buy the milk' };
    const task_two = { key: v4(), name: 'buy the milk' };
    store.dispatch(todolistFetched([task_one, task_two]));

    expect(selectTodolistPage(store.getState())).toEqual({ statut: 'atLeastOneTask', tasks: [task_one, task_two] });
  });
});


