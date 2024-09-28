from uuid import UUID, uuid4


def an_id(index: int | None = None):
    if index:
        return index
    return uuid4()
