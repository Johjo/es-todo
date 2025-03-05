import { match } from 'ts-pattern';
import { useDispatch, useSelector } from 'react-redux';
import type { Task } from '../../../../hexagon/todolistPage.slice.ts';
import { selectTodolistPage } from '../../../../hexagon/todolistPage.slice.ts';
import { useEffect, useState } from 'react';
import { fetchTodolist } from '../../../../hexagon/fetchTodolist.usecase.ts';
import { openTask } from '../../../../hexagon/openTask.usecase.ts';
import type { AppDispatch } from '../../../../hexagon/store.ts';


export function TaskForm() {
  const dispatch = useDispatch<AppDispatch>()
  const [taskName, setTaskName] = useState('');

  return <>
    <input type="text" value={taskName} onChange={(e) => setTaskName(e.target.value)} />
    <button onClick={() => dispatch(openTask(taskName))}>Add task</button>
  </>;
}

export function TodolistPage() {
  const dispatch = useDispatch<AppDispatch>()

  useEffect(() => {
    void dispatch(fetchTodolist());
  }, []);

  return <>
    <TaskForm />
    <TodolistPageDisplay />
  </>;
}

export function TodolistPageDisplay() {
  const todolistPage = useSelector(selectTodolistPage);

  return match(todolistPage)
    .with({ statut: 'idle' }, () => <></>)
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

