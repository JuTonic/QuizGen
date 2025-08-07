from dataclasses import dataclass
from typing import Generic

from modules.utils.types import A, C, Q, V
from modules.variant_builder.task_pool import QTaskPool
from modules.variant_builder.variant_set import QVariantSet


@dataclass
class QuizGen(Generic[C, V, Q, A]):
    task_pool: QTaskPool[C, V, Q, A]
    previos_variants: QVariantSet[C, V, Q, A]
