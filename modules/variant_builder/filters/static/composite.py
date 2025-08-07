from collections.abc import Iterable
from dataclasses import dataclass, field, replace
from typing import Self, override

from modules.task import QTask
from modules.utils.types import A, C, Q, V
from modules.variant_builder.filters.static import FilterStatic


@dataclass(frozen=True)
class CompositeFilterStatic(FilterStatic[C, V, Q, A]):
    filters: list[FilterStatic[C, V, Q, A]]
    is_inverted: bool = field(default=False)

    @override
    def is_satisfied(self, task: QTask[C, V, Q, A]) -> bool:
        if not self.is_inverted:
            return all(filter.is_satisfied(task) for filter in self.filters)
        else:
            return any(not filter.is_satisfied(task) for filter in self.filters)

    @override
    def invert(self) -> "CompositeFilterStatic[C, V, Q, A]":
        return replace(self, is_inverted=not self.is_inverted)

    @override
    def __invert__(self) -> "CompositeFilterStatic[C, V, Q, A]":
        return self.invert()
