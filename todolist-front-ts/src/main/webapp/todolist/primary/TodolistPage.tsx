import { match } from 'ts-pattern';
import { useSelector, useStore } from 'react-redux';
import type { Task } from '../../../../hexagon/todolistPage.ts';
import { selectTodolistPage, todolistFetched } from '../../../../hexagon/todolistPage.ts';
import type { AppStore } from '../../../../hexagon/store.ts';
import { useEffect } from 'react';


export function TodolistPage() {
  const store = useStore<AppStore>();

  useEffect(() => {
    store.dispatch(todolistFetched({ tasks: [] }));
  }, []);

  return <TodolistPageDisplay />;
}

export function TodolistPageDisplay() {
  const todolistPage = useSelector(selectTodolistPage);

  return match(todolistPage)
    .with({ statut: 'loading' }, () => <Loading />)
    .with({ statut: 'empty' }, () => <EmptyState />)
    .with({ statut: 'atLeastOneTask' }, (todolist) => <Todolist tasks={todolist.tasks} />)
    .exhaustive();
}

function EmptyState() {
  return <p>no task...</p>;
}

function Loading() {
  return <p>loading...</p>;
}

interface TodolistProps {
  tasks: Task[];
}

function Todolist({ tasks }: TodolistProps) {
  return <ul>{tasks.map(task => <Task key={task.key} task={task} />)}</ul>;
}

interface TaskProps {
  task: Task;
}

function Task({ task }: TaskProps) {
  return <li>{task.name}</li>;
}

