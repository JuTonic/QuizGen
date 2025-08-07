from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, Protocol

from modules.task import QTask
from modules.utils.types import A, C, Q, V
from modules.variant_builder.context import DynamicCtx
from modules.variant_builder.task_pool import QTaskPool


class QTaskSelector(ABC, Generic[C, V, Q, A]):
    @abstractmethod
    def select(
        self, filtered_tasks: list[QTask[C, V, Q, A]], ctx: DynamicCtx[C, V, Q, A]
    ) -> QTask[C, V, Q, A]: ...
