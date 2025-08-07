import uuid
from dataclasses import dataclass, field
from typing import Generic

from option import Option

from modules.utils.types import C, V


@dataclass(frozen=True)
class QTaskFactoryMetadata(Generic[C, V]):
    name: Option[str] = field(default=Option[str].maybe(None))
    description: Option[str] = field(default=Option[str].maybe(None))
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    @staticmethod
    def from_values(
        name: str | None = None,
        description: str | None = None,
    ) -> "QTaskFactoryMetadata[C, V]":
        return QTaskFactoryMetadata(
            name=Option[str].maybe(name),
            description=Option[str].maybe(description),
        )
