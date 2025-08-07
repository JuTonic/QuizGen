import uuid
from collections.abc import Iterable
from dataclasses import field
from typing import overload, override

from modules.task import QTask
from modules.utils.types import A, C, Q, V
from modules.variant_builder.filters.static import FilterStatic
from modules.variant_builder.filters.types import QTaskOrFactory


class MustBeOneOfFilter(FilterStatic[C, V, Q, A]):
    must_be_one_of: list[uuid.UUID] = field(default_factory=list[uuid.UUID])

    @overload
    def __init__(self, item: Iterable[QTaskOrFactory[C, V, Q, A]]) -> None: ...

    @overload
    def __init__(
        self, item: QTaskOrFactory[C, V, Q, A], **kwargs: QTaskOrFactory[C, V, Q, A]
    ) -> None: ...

    def __init__(
        self,
        item: Iterable[QTaskOrFactory[C, V, Q, A]] | QTaskOrFactory[C, V, Q, A],
        **kwargs: QTaskOrFactory[C, V, Q, A],
    ):
        if isinstance(item, Iterable):
            self.must_be_one_of.extend(map(lambda i: i.id, item))
        else:
            self.must_be_one_of.append(item.id)
        self.must_be_one_of.extend(map(lambda i: i.id, kwargs.values()))

    @override
    def is_satisfied(self, task: QTask[C, V, Q, A]) -> bool:
        task_id = task.id
        factory_id = task.factory_metadata.map(lambda m: m.id).unwrap_or(None)
        return any(task_id == id or factory_id == id for id in self.must_be_one_of)
