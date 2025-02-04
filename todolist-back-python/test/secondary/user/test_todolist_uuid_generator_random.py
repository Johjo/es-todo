from src.secondary.user.todolist_uuid_generator_random import TodolistUuidGeneratorRandom


class TestTodolistUuidGeneratorRandom:
    def test_generate_random_todolist_key(self):
        sut = TodolistUuidGeneratorRandom()
        assert sut.generate_todolist_key() != sut.generate_todolist_key()
