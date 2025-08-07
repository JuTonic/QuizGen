from dataclasses import dataclass, field, replace
from typing import override

from modules.task import QTask
from modules.utils.types import A, C, Q, V
from modules.variant_builder.context import DynamicCtx
from modules.variant_builder.filters.dynamic import FilterDynamic


@dataclass
class CompositeFilterDynamic(FilterDynamic[C, V, Q, A]):
    filters: list[FilterDynamic[C, V, Q, A]]
    is_inverted: bool = field(default=False)

    @override
    def check_if_satisfied(
        self, task: QTask[C, V, Q, A], ctx: DynamicCtx[C, V, Q, A]
    ) -> bool:
        return all(filter.check_if_satisfied(task, ctx) for filter in self.filters)

    @override
    def invert(self) -> "CompositeFilterDynamic[C, V, Q, A]":
        return replace(self, is_inverted=not self.is_inverted)

    @override
    def __invert__(self) -> "CompositeFilterDynamic[C, V, Q, A]":
        return self.invert()
