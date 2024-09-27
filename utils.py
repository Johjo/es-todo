class SharedInstanceBuiltIn:
    _instances = {}  # type: ignore

    @classmethod
    def get_shared_instance(cls):
        if cls not in cls._instances:
            cls._instances[cls] = cls()
        return cls._instances[cls]
