from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Callable, Generic, Self, overload, override

from modules.tag import Tag, Tags
from modules.utils.types import A, C, Q, V
from modules.variant_builder.filters import Filter
from modules.variant_builder.filters.dynamic import FilterDynamic
from modules.variant_builder.filters.static import FilterStatic
from modules.variant_builder.filters.static.must_be_one_of import MustBeOneOfFilter
from modules.variant_builder.filters.static.must_include_all_tags import (
    MustIncludeAllTagsFilter,
)
from modules.variant_builder.filters.static.must_include_any_tag import (
    MustIncludeAnyTagFilter,
)
from modules.variant_builder.filters.types import QTaskOrFactory


@dataclass
class FilterBuilder(Generic[C, V, Q, A]):
    static_filters: list[FilterStatic[C, V, Q, A]] = field(default_factory=list)
    dynamic_filters: list[FilterDynamic[C, V, Q, A]] = field(default_factory=list)

    def add_static(self, filter: FilterStatic[C, V, Q, A]) -> Self:
        self.static_filters.append(filter)
        return self

    def add_dynamic(self, filter: FilterDynamic[C, V, Q, A]) -> Self:
        self.dynamic_filters.append(filter)
        return self

    def add(self, filter: FilterStatic[C, V, Q, A] | FilterDynamic[C, V, Q, A]) -> Self:
        if isinstance(filter, FilterStatic):
            self.static_filters.append(filter)
        else:
            self.dynamic_filters.append(filter)
        return self

    def __call__(
        self, filter: FilterStatic[C, V, Q, A] | FilterDynamic[C, V, Q, A]
    ) -> Self:
        return self.add(filter)

    @overload
    def be_one_of(self, item: Iterable[QTaskOrFactory[C, V, Q, A]]) -> Self: ...

    @overload
    def be_one_of(
        self, item: QTaskOrFactory[C, V, Q, A], **kwargs: QTaskOrFactory[C, V, Q, A]
    ) -> Self: ...

    def be_one_of(
        self,
        item: Iterable[QTaskOrFactory[C, V, Q, A]] | QTaskOrFactory[C, V, Q, A],
        **kwargs: QTaskOrFactory[C, V, Q, A],
    ) -> Self:
        return self.add_static(MustBeOneOfFilter(item, **kwargs))

    @overload
    def include_any_tag(self, tag: Tags[C, V]) -> Self: ...

    @overload
    def include_any_tag(self, tag: Iterable[Tag[C, V]]) -> Self: ...

    @overload
    def include_any_tag(self, tag: Tag[C, V], **kwargs: Tag[C, V]) -> Self: ...

    def include_any_tag(
        self,
        tag: Tags[C, V] | Tag[C, V] | Iterable[Tag[C, V]],
        **kwargs: Tag[C, V],
    ) -> Self:
        return self.add_static(MustIncludeAnyTagFilter(tag, **kwargs))

    @overload
    def include_all_tags(self, tag: Tags[C, V]) -> Self: ...

    @overload
    def include_all_tags(self, tag: Iterable[Tag[C, V]]) -> Self: ...

    @overload
    def include_all_tags(self, tag: Tag[C, V], **kwargs: Tag[C, V]) -> Self: ...

    def include_all_tags(
        self,
        tag: Tags[C, V] | Tag[C, V] | Iterable[Tag[C, V]],
        **kwargs: Tag[C, V],
    ) -> Self:
        return self.add_static(MustIncludeAllTagsFilter(tag, **kwargs))

    @overload
    def include_tag(self, category: C, value: V) -> Self: ...

    @overload
    def include_tag(self, category: Tag[C, V], value: None = None) -> Self: ...

    def include_tag(self, category: C | Tag[C, V], value: V | None = None) -> Self:
        if isinstance(category, Tag):
            return self.include_all_tags(category)
        else:
            assert value is not None
            return self.include_all_tags([Tag(category, value)])

    def be_inverse_of(
        self,
        filter: Callable[["FilterBuilder[C, V, Q, A]"], "FilterBuilder[C, V, Q, A]"],
    ) -> "FilterBuilder[C, V, Q, A]":
        return filter(FilterBuilder[C, V, Q, A]()).invert()

    def build(self) -> Filter[C, V, Q, A]:
        return Filter(self.static_filters, self.dynamic_filters)

    def invert(self) -> Self:
        for i in range(len(self.static_filters)):
            self.static_filters[i] = ~self.static_filters[i]
        for i in range(len(self.dynamic_filters)):
            self.dynamic_filters[i] = ~self.dynamic_filters[i]
        return self

    def __invert__(self) -> Self:
        return self.invert()
