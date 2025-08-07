from dataclasses import dataclass, field
from typing import Generic

from modules.task import QTask
from modules.utils.types import A, C, Q, V
from modules.variant import QVariant
from modules.variant_builder.task_pool import QTaskPool
from modules.variant_builder.variant_set import QVariantSet


@dataclass
class DynamicCtx(Generic[C, V, Q, A]):
    task_pool: QTaskPool[C, V, Q, A]
    previous_variants: QVariantSet[C, V, Q, A] = field(
        default_factory=QVariantSet[C, V, Q, A]
    )
    current_variant_tasks: list[QTask[C, V, Q, A]] = field(default_factory=list)
