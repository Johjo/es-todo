from dataclasses import dataclass, replace

from expression import Result, Error, Ok


@dataclass(frozen=True)
class TaskKey:
    value: int


@dataclass
class TaskSnapshot:
    key: TaskKey
    name: str
    is_open: bool


@dataclass
class TodolistSnapshot:
    name: str
    tasks: list[TaskSnapshot]


@dataclass(frozen=True)
class Task:
    key: TaskKey
    name: str
    is_open: bool

    def to_snapshot(self) -> TaskSnapshot:
        return TaskSnapshot(key=self.key, name=self.name, is_open=self.is_open)

    @classmethod
    def from_snapshot(cls, snapshot: TaskSnapshot) -> 'Task':
        return Task(key=snapshot.key, name=snapshot.name, is_open=snapshot.is_open)

    def reword(self, new_name) -> 'Task':
        return replace(self, name=new_name)

    def close_task(self) -> 'Task':
        return replace(self, is_open=False)


@dataclass(frozen=True)
class TodolistAggregate:
    name: str
    tasks: tuple[Task, ...]

    @classmethod
    def create(cls, todolist_name) -> 'TodolistAggregate':
        return TodolistAggregate(name=todolist_name, tasks=())

    @classmethod
    def from_snapshot(cls, snapshot: TodolistSnapshot) -> 'TodolistAggregate':
        return TodolistAggregate(name=snapshot.name, tasks=(*[Task.from_snapshot(task) for task in snapshot.tasks],))

    def to_snapshot(self) -> TodolistSnapshot:
        return TodolistSnapshot(self.name, tasks=[task.to_snapshot() for task in self.tasks])

    def open_task(self, task: Task) -> Result['TodolistAggregate', str]:
        return Ok(replace(self, tasks=self.tasks + (task,)))

    def close_task(self, key) -> Result['TodolistAggregate', str]:
        if not [task for task in self.tasks if task.key == key]:
            return Error(f"The task '{key}' does not exist")
        return Ok(replace(self, tasks=(*[task.close_task() if task.key == key else task for task in self.tasks],)))

    def reword_task(self, key: TaskKey, new_name: str) -> Result['TodolistAggregate', str]:
        if not [task for task in self.tasks if task.key == key]:
            return Error(f"The task '{key}' does not exist")

        return Ok(replace(self, tasks=(*[task.reword(new_name) if task.key == key else task for task in self.tasks],)))

    def import_tasks(self, task_snapshots: list[TaskSnapshot]) -> Result['TodolistAggregate', str]:
        return Ok(replace(self, tasks=self.tasks + (*[Task.from_snapshot(snapshot) for snapshot in task_snapshots],)))

