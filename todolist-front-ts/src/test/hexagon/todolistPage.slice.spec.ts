import { v4 } from 'uuid';
import { selectTodolistPage, todolistPageDisplayed } from '../../hexagon/todolistPage.slice';
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
    store.dispatch(todolistPageDisplayed({statut : 'empty'}));

    expect(selectTodolistPage(store.getState())).toEqual({ statut: 'empty' });
  });

  it('should fetch at least one task', () => {
    const task_one = {key: v4(), name: "buy the milk"};
    const task_two = {key: v4(), name: "buy the milk"};
    store.dispatch(todolistPageDisplayed({ statut: 'atLeastOneTask', tasks:[task_one, task_two] }));

    expect(selectTodolistPage(store.getState())).toEqual({ statut: 'atLeastOneTask', tasks:[task_one, task_two] });
  });
});


