from dataclasses import dataclass, field
from typing import Generic

from modules.utils.types import A, C, Q, V
from modules.variant import QVariant


@dataclass
class QVariantSet(list[QVariant[C, V, Q, A]], Generic[C, V, Q, A]): ...
