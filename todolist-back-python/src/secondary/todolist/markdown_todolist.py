import re

from src.hexagon.todolist.write.import_many_task import ExternalTodoListPort, TaskImported


class MarkdownTodolist(ExternalTodoListPort):
    def __init__(self, markdown: str) -> None:
        self._markdown = markdown

    def all_tasks(self) -> list[TaskImported]:
        pattern = r"- \[([x ])\] (.+)"
        all_tasks = re.findall(pattern, self._markdown)
        return [TaskImported(name=task[1], is_open=task[0]!="x") for task in all_tasks]  # type: ignore
