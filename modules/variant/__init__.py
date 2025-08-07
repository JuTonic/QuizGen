from dataclasses import dataclass, field
from typing import Generic

from modules.task import QTask
from modules.utils.types import A, C, Q, V


@dataclass
class QVariant(Generic[C, V, Q, A]):
    tasks: list[QTask[C, V, Q, A]] = field(default_factory=list)

    def __iter__(self):
        for task in self.tasks:
            yield task
