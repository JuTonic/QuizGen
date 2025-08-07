from dataclasses import dataclass
from typing import Generic

from modules.utils.types import A, C, Q, V
from modules.variant_builder.filters.dynamic import FilterDynamic
from modules.variant_builder.filters.dynamic.composite import CompositeFilterDynamic
from modules.variant_builder.filters.static import FilterStatic
from modules.variant_builder.filters.static.composite import CompositeFilterStatic


class Filter(Generic[C, V, Q, A]):
    static: FilterStatic[C, V, Q, A]
    dynamic: FilterDynamic[C, V, Q, A]

    def __init__(
        self,
        static: CompositeFilterStatic[C, V, Q, A] | list[FilterStatic[C, V, Q, A]],
        dynamic: CompositeFilterDynamic[C, V, Q, A] | list[FilterDynamic[C, V, Q, A]],
    ):
        if isinstance(static, list):
            self.static = CompositeFilterStatic(static)
        else:
            self.static = static

        if isinstance(dynamic, list):
            self.dynamic = CompositeFilterDynamic(dynamic)
        else:
            self.dynamic = dynamic
