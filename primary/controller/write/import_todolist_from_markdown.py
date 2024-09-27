from domain.todo_markdown_importer import TodoMarkdownImporter
from primary.controller.dependency_list import DependencyList


def import_todolist_from_markdown(todolist_name, markdown, dependencies: DependencyList):
    todo_writer = dependencies.todo_writer_from_import_todolist_from_markdown(todolist_name)
    TodoMarkdownImporter(todo_writer).import_from_markdown(markdown)

