from dataclasses import dataclass, field
from typing import Generic

from option import Option

from modules.utils.types import A, C, Q, V
from modules.variant_builder.filters import Filter
from modules.variant_builder.filters.builder import FilterBuilder


class VariantTask(Generic[C, V, Q, A]):
    must: FilterBuilder[C, V, Q, A]

    def __init__(self):
        self.must = FilterBuilder[C, V, Q, A]()
