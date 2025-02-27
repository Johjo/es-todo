import { match } from 'ts-pattern';
import { useSelector } from 'react-redux';
import type { Task } from '../../../../hexagon/todolistPage.slice.ts';
import { selectTodolistPage } from '../../../../hexagon/todolistPage.slice.ts';
import { useEffect, useState } from 'react';
import { useDependenciesUseCase } from './useDependenciesUseCase.ts';


export function TaskForm() {
  const dependenciesUseCase = useDependenciesUseCase();
  const [taskName, setTaskName] = useState("");

  return <>
    <input type="text" value={taskName} onChange={(e) => setTaskName(e.target.value)} />
    <button onClick={() => dependenciesUseCase.openTask().execute(taskName).then()}>Add task</button>
  </>;
}

export function TodolistPage() {
  const dependenciesUseCase = useDependenciesUseCase();

  useEffect(() => {
    void dependenciesUseCase.todolistPageDisplay().execute();
  }, []);

  return <><TaskForm /><TodolistPageDisplay /> </>;
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

