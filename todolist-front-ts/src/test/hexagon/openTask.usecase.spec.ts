// ajouter une tache dans les tâches
// mettre à jour la vue des tâches
import { v4 } from 'uuid';
import { openTask, OpenTaskUseCase } from '../../hexagon/openTask.usecase';
import { ToBackend, TodolistUpdaterPort, UuidGeneratorPort } from '../../hexagon/openTask.port';
import { AppStore, createAppStore } from '../../hexagon/store';

describe('open task use case', () => {
  let store: AppStore;
  let uuidGenerator: UuidGeneratorForTest;
  let todolistUpdater: TodolistUpdaterForTest;
  let useCase: OpenTaskUseCase;

  beforeEach(() => {
    uuidGenerator = new UuidGeneratorForTest();
    todolistUpdater = new TodolistUpdaterForTest();
    useCase = new OpenTaskUseCase(uuidGenerator, todolistUpdater);
    store = createAppStore({ uuidGenerator, todolistUpdater, openTask : useCase });
  });

  it('should do nothing', async () => {
    expect(todolistUpdater.all()).toEqual([]);
  });

  it('should add task to todolist', async () => {
    // GIVEN
    const taskKey = v4();
    uuidGenerator.feed(taskKey);
    // WHEN
    await store.dispatch(openTask('buy the milk'));
    // THEN
    expect(todolistUpdater.all()).toEqual([{ key: taskKey, name: 'buy the milk' }]);
  });

  it('should update todolist in store', async () => {
    // GIVEN
    const task = { key: v4(), name: 'buy the milka' };
    uuidGenerator.feed(task.key);

    // WHEN
    await store.dispatch(openTask(task.name));

    // THEN
    expect(todolistUpdater.all()).toEqual([{ key: task.key, name: task.name }]);

    expect(store.getState().todolistPage).toEqual({
      statut: 'atLeastOneTask',
      tasks: [{ key: task.key, name: task.name }]
    });
  });
});

class TodolistUpdaterForTest implements TodolistUpdaterPort {
  private tasks: ToBackend.Task[] = [];

  all() {
    return [...this.tasks];
  }

  async openTask(_todolistKey: string, task: ToBackend.Task): Promise<void> {
    this.tasks.push(task);
  }
}

class UuidGeneratorForTest implements UuidGeneratorPort {
  private nextKey: string | undefined = undefined;

  feed(nextKey: string) {
    this.nextKey = nextKey;
  }

  generate() {
    if (this.nextKey === undefined) {
      throw new Error('UuidGeneratorForTest.generate() should be called after feed()');
    }

    return this.nextKey;
  }
}
