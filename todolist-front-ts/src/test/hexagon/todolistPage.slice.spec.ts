import { v4 } from 'uuid';
import {
  emptyTodolistFetched,
  selectTodolistPage,
  taskOpened,
  todolistFetched,
  todolistFetchingStarted
} from '../../hexagon/todolistPage.slice';
import { AppStore, createAppStore } from '../../hexagon/store';


describe('Todolist', () => {
  let store: AppStore;
  beforeEach(() => {
    store = createAppStore({});
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

  describe('taskOpened', () => {
    it('should open task when loading', () => {
      let taskKey = v4();
      store.dispatch(taskOpened({ key: taskKey, name: 'buy the milk' }));

      expect(selectTodolistPage(store.getState())).toEqual({
        statut: 'atLeastOneTask',
        tasks: [{ key: taskKey, name: 'buy the milk' }]
      });
    });

    it('should open task when task', () => {
      // GIVEN
      const task_one = { key: v4(), name: 'buy the milk' };
      const task_two = { key: v4(), name: 'buy the water' };

      store.dispatch(todolistFetched([task_one]));

      // WHEN
      store.dispatch(taskOpened({ key: task_two.key, name: task_two.name }));

      // THEN
      expect(selectTodolistPage(store.getState())).toEqual({
        statut: 'atLeastOneTask',
        tasks: [
          { key: task_one.key, name: task_one.name },
          { key: task_two.key, name: task_two.name }]
      });
    });
  });

});


