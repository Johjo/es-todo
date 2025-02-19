import { TodolistFetcher } from '../../secondary/todolistFetcher';

describe('todolistFetcher', () => {
  it('fetch todolist', async () => {
    const sut = new TodolistFetcher();
    const actual = await sut.getTodolist();

    expect(actual).toEqual({ tasks: [] });
  });
});
