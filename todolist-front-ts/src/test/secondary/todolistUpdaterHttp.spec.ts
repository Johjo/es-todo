import { TodolistFetcherHttp } from '../../secondary/todolistFetcherHttp';
import { v4 } from 'uuid';
import { Task } from '../../hexagon/todolistPage.slice';
import { FromBackend } from '../../hexagon/todolistPageDisplay.usecase';
import { TodolistUpdaterHttp } from '../../secondary/todolistUpdaterHttp';

const url = 'http://todolist-ytreza-dev.osc-fr1.scalingo.io';

async function deleteTodolist(todolistKey: string) {
  await fetch(`${url}/todolist/${todolistKey}`, { method: 'DELETE' });
}


describe('todolist update http', () => {
  it('should update todolist', async () => {
    const task = { key: v4(), name: `buy the milk - ${v4()}` };
    const todolistKey = `64327d1c-8b58-4ccf-9b9f-f954e7f5a72a`;
    await deleteTodolist(todolistKey);

    await createTodolist(todolistKey);
    const sut = new TodolistUpdaterHttp(url);
    await sut.openTask(todolistKey, { ...task });

    expect(await fetchTodolist(todolistKey)).toEqual({ tasks: [{ ...task }] });
  });

});


describe.skip('todolistFetcher', () => {
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


async function fetchTodolist(todolistKey: string): Promise<FromBackend.Todolist> {
  const response = await fetch(`${url}/todolist/${todolistKey}/task`, {
    method: 'GET',
    headers: {
      'Access-Control-Allow-Origin': '*'

    }
  });
  const todolist = await response.json() as FromBackend.Todolist;
  if (todolist.tasks.length === 0) {
    return { tasks: [] };
  }

  return {
    tasks: todolist.tasks.map(taskBackEnd => {
      return { key: taskBackEnd.key, name: taskBackEnd.name };
    })
  };

}
