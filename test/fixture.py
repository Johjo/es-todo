from uuid import UUID, uuid4


def an_id(index: int | None = None):
    if index:
        return UUID(int=index, version=4)
    return uuid4()
