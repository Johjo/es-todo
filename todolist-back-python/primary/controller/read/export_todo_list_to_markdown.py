from domain.todo_markdown_exporter import TodoMarkdownExporter
from primary.controller.dependency_list import DependencyList


def export_todo_list_to_markdown(name, dependencies: DependencyList):
    todo_reader = dependencies.todo_reader_for_todo_markdown_exporter(name)
    return TodoMarkdownExporter(todo_reader).export_to_markdown()


