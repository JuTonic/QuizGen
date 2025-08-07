from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, override, runtime_checkable

from modules.task import QTask
from modules.utils.types import A, C, Q, V


class FilterStatic(ABC, Generic[C, V, Q, A]):
    @abstractmethod
    def is_satisfied(self, task: QTask[C, V, Q, A]) -> bool: ...

    def __invert__(self) -> "FilterStatic[C, V, Q, A]":
        return StaticFilterNegator(self)

    def invert(self) -> "FilterStatic[C, V, Q, A]":
        return StaticFilterNegator(self)


@dataclass(frozen=True)
class StaticFilterNegator(FilterStatic[C, V, Q, A]):
    filter: FilterStatic[C, V, Q, A]

    @override
    def is_satisfied(self, task: QTask[C, V, Q, A]) -> bool:
        return not self.filter.is_satisfied(task)

    @override
    def __invert__(self) -> "FilterStatic[C, V, Q, A]":
        return self.filter

    @override
    def invert(self) -> "FilterStatic[C, V, Q, A]":
        return self.filter
