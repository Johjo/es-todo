// ajouter une tache au backedn
// ajouter une tache dans les tâches
// mettre à jour la vue des tâches
import { v4 } from 'uuid';

class OpenTaskUseCase {
  constructor(private readonly uuidGenerator: UuidGeneratorForTest, private readonly todolistUpdater: TodolistUpdaterForTest) {

  }

  async execute(taskName: string) {
    this.todolistUpdater.openTask({ key: this.uuidGenerator.generate(), name: taskName });
  }
}

namespace ToBackend {
  export type Task = { key: string, name: string };
}

class TodolistUpdaterForTest {
  private tasks: ToBackend.Task[] = [];

  all() {
    return [...this.tasks];
  }

  openTask(task: { key: string; name: string }) {
    this.tasks.push(task);
  }
}

class UuidGeneratorForTest {
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

describe('open task use case', () => {
  let uuidGenerator: UuidGeneratorForTest;
  let todolistUpdater: TodolistUpdaterForTest;
  let sut: OpenTaskUseCase;

  beforeEach(() => {
    uuidGenerator = new UuidGeneratorForTest();
    todolistUpdater = new TodolistUpdaterForTest();
    sut = new OpenTaskUseCase(uuidGenerator, todolistUpdater);
  });
  it('should do nothing', async () => {
    expect(todolistUpdater.all()).toEqual([]);
  });

  it('should add task to todolist', async () => {
    // GIVEN
    const taskKey = v4();
    uuidGenerator.feed(taskKey);
    // WHEN
    await sut.execute('buy the milk');
    // THEN
    expect(todolistUpdater.all()).toEqual([{ key: taskKey, name: 'buy the milk' }]);
  });
});
