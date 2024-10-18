from uuid import UUID, uuid4

from hexagon.fvp.type import TaskKey


def a_task_key(index: TaskKey | UUID | int | None = None) -> TaskKey:
    if isinstance(index, int):
        return TaskKey(UUID(int=index))
    if isinstance(index, UUID):
        return TaskKey(index)
    return TaskKey(uuid4())
