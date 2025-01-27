from src.dependencies import Dependencies
from src.infra.fvp_memory import FvpMemory
from src.infra.memory import Memory


def inject_infrastructure_in_memory(dependencies: Dependencies, memory: Memory, fvp_memory: FvpMemory) -> Dependencies:
    dependencies = dependencies.feed_infrastructure(Memory, lambda _: memory)
    dependencies = dependencies.feed_infrastructure(FvpMemory, lambda _: fvp_memory)
    return dependencies
