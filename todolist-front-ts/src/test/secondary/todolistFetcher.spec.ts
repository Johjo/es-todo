import { TodolistFetcherHttp } from '../../secondary/todolistFetcherHttp';
import { v4 } from 'uuid';
import { Task } from '../../hexagon/todolistPage.slice';

const url = 'http://todolist-ytreza-dev.osc-fr1.scalingo.io';

async function deleteTodolist(todolistKey: string) {
  await fetch(`${url}/todolist/${todolistKey}`, { method: 'DELETE' });
}

describe('todolistFetcher', () => {
  it('fetch unknown todolist', async () => {
    const sut = new TodolistFetcherHttp(url);
    const actual = await sut.getTodolist(v4());

    expect(actual).toEqual({ tasks: [] });
  });

  it('fetch todolist with tasks', async () => {
    const todolistKey = `21827d1c-8b58-4ccf-9b9f-f954e7f5a72a`;
    await deleteTodolist(todolistKey);
    await createTodolist(todolistKey);
    const task_one = await feedTask(todolistKey, aTask());
    const task_two = await feedTask(todolistKey, aTask());
    const sut = new TodolistFetcherHttp(url);
    const actual = await sut.getTodolist(todolistKey);
    expect(actual).toEqual({ tasks: [task_one, task_two] });
  });

});

function aTask() {
  return { key: v4(), name: `buy the milk - ${v4()}` };
}

async function createTodolist(todolistKey: string) {
  let finalUrl = `${url}/todolist/${todolistKey}`;
  await fetch(finalUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json;charset=UTF-8' },
    body: JSON.stringify({ name: `my todolist` })
  });
}

async function feedTask(todolistKey: string, task: Task) {
  let finalUrl = `${url}/todolist/${todolistKey}/task/${task.key}`;
  await fetch(finalUrl, {
    method: 'POST',
    headers: { 'content-type': 'application/json;charset=UTF-8' },
    body: JSON.stringify({ name: task.name })
  });
  return task;
}
