from collections.abc import Iterable
from dataclasses import field
from typing import overload, override

from modules.tag import Tag, Tags
from modules.task import QTask
from modules.utils.types import A, C, Q, V
from modules.variant_builder.filters.static import FilterStatic


class MustIncludeAllTagsFilter(FilterStatic[C, V, Q, A]):
    tags: Tags[C, V] = field(default_factory=Tags[C, V])

    @overload
    def __init__(self, tag: Tags[C, V]) -> None: ...

    @overload
    def __init__(self, tag: Iterable[Tag[C, V]]) -> None: ...

    @overload
    def __init__(self, tag: Tag[C, V], **kwargs: Tag[C, V]) -> None: ...

    def __init__(
        self,
        tag: Tags[C, V] | Tag[C, V] | Iterable[Tag[C, V]],
        **kwargs: Tag[C, V],
    ):
        if isinstance(tag, Tags):
            self.tags = tag
        elif isinstance(tag, Iterable):
            self.tags = Tags[C, V](tag)
        else:
            self.tags = Tags[C, V](kwargs.values())
            self.tags.add_tag(tag)

    @override
    def is_satisfied(self, task: QTask[C, V, Q, A]) -> bool:
        return all(task.tags.has_tag(tag) for tag in self.tags)
