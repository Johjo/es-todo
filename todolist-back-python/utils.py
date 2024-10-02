class SharedInstanceBuiltIn:
    _instances = {}  # type: ignore

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def get_shared_instance(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = cls(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def set_shared_instance(cls, instance):
        cls._instances[cls] = instance
