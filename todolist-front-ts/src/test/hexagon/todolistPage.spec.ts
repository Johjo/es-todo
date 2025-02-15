import { v4 } from 'uuid';
import { selectTodolistPage, todolistFetched } from '../../hexagon/todolistPage';
import { AppStore, createStore } from '../../hexagon/store';


describe('Todolist', () => {
  let store: AppStore;
  beforeEach(() => {
    store = createStore();
  });

  it('initial state should be loading', () => {
    expect(selectTodolistPage(store.getState())).toEqual({ statut: 'loading' });
  });

  it('should fetch empty todolist', () => {
    store.dispatch(todolistFetched({ tasks: [] }));

    expect(selectTodolistPage(store.getState())).toEqual({ statut: 'empty' });
  });

  it('should fetch at least one task', () => {
    const task_one = {key: v4(), name: "buy the milk"};
    const task_two = {key: v4(), name: "buy the milk"};
    store.dispatch(todolistFetched({ tasks: [task_one, task_two] }));

    expect(selectTodolistPage(store.getState())).toEqual({ statut: 'atLeastOneTask', tasks:[task_one, task_two] });
  });
});


