from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Protocol, override, runtime_checkable

from modules.task import QTask
from modules.utils.types import A, C, Q, V
from modules.variant import QVariant
from modules.variant_builder.context import DynamicCtx
from modules.variant_builder.task_pool import QTaskPool
from modules.variant_builder.variant_set import QVariantSet


class FilterDynamic(ABC, Generic[C, V, Q, A]):
    @abstractmethod
    def check_if_satisfied(
        self, task: QTask[C, V, Q, A], ctx: DynamicCtx[C, V, Q, A]
    ) -> bool: ...

    def __invert__(self) -> "FilterDynamic[C, V, Q, A]":
        return DynamicFilterNegator(self)

    def inverse(self) -> "FilterDynamic[C, V, Q, A]":
        return DynamicFilterNegator(self)

    def invert(self) -> "FilterDynamic[C, V, Q, A]":
        return DynamicFilterNegator(self)


@dataclass(frozen=True)
class DynamicFilterNegator(FilterDynamic[C, V, Q, A]):
    filter: FilterDynamic[C, V, Q, A]

    @override
    def check_if_satisfied(
        self, task: QTask[C, V, Q, A], ctx: DynamicCtx[C, V, Q, A]
    ) -> bool:
        return not self.filter.check_if_satisfied(task, ctx)

    @override
    def __invert__(self) -> "FilterDynamic[C, V, Q, A]":
        return self.filter

    @override
    def invert(self) -> "FilterDynamic[C, V, Q, A]":
        return self.filter
