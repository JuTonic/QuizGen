import uuid
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Generic, override

from option import Option

from modules.tag import Tag, Tags
from modules.utils.types import A, C, Q, V
from modules.utils.utils import indent

if TYPE_CHECKING:
    from modules.task.factory.metadata import QTaskFactoryMetadata


@dataclass
class QTask(Generic[C, V, Q, A]):
    question: Q
    answer: A
    tags: Tags[C, V]
    id: uuid.UUID
    factory_metadata: Option["QTaskFactoryMetadata[C, V]"] = Option[
        "QTaskFactoryMetadata[C, V]"
    ].maybe(None)

    def __init__(
        self,
        question: Q,
        answer: A = None,
        tags: Tags[C, V] | list[Tag[C, V]] | Tag[C, V] | None = None,
    ):
        self.question = question
        self.answer = answer
        if isinstance(tags, Tag):
            self.tags = Tags[C, V]([tags])
        if isinstance(tags, list):
            self.tags = Tags[C, V](tags)
        elif isinstance(tags, Tags):
            self.tags = tags
        self.id = uuid.uuid4()

    @override
    def __str__(self) -> str:
        return f"Question:\n{indent(str(self.question))}\nAnswer:\n{indent(str(self.answer))}\nTags:\n{indent(str(self.tags))}"
