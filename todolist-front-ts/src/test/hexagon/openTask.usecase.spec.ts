import { v4 } from 'uuid';
import { openTask, OpenTaskPrimaryPort, OpenTaskUseCase } from '../../hexagon/openTask.usecase';
import { OpenTaskUpdaterPort, ToBackend, UuidGeneratorPort } from '../../hexagon/openTask.port';
import { AppDispatch, AppStore, createAppStore } from '../../hexagon/store';
import { DependenciesUseCaseDummy } from '../dependenciesUseCaseDummy';

class DependenciesForTest extends DependenciesUseCaseDummy {
  constructor(private readonly uuidGenerator: UuidGeneratorForTest, private readonly todolistUpdater: TodolistUpdaterForTest) {
    super();
    console.log(this.uuidGenerator);
  }

  openTask(dispatch: AppDispatch): OpenTaskPrimaryPort {
    return new OpenTaskUseCase(this.uuidGenerator, this.todolistUpdater, dispatch);
  }

}

describe('open task use case', () => {
  let store: AppStore;
  let uuidGenerator: UuidGeneratorForTest;
  let todolistUpdater: TodolistUpdaterForTest;

  beforeEach(() => {
    uuidGenerator = new UuidGeneratorForTest();
    todolistUpdater = new TodolistUpdaterForTest();
    store = createAppStore(new DependenciesForTest(uuidGenerator, todolistUpdater));
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

class TodolistUpdaterForTest implements OpenTaskUpdaterPort {
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
