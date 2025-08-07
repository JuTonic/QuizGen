import uuid
from abc import ABC, abstractmethod
from typing import Callable, Generic

from option import Option

from modules.task import QTask
from modules.task.factory.metadata import QTaskFactoryMetadata
from modules.utils.types import A, C, Q, V


class QTaskFactory(ABC, Generic[C, V, Q, A]):
    id: uuid.UUID
    metadata: QTaskFactoryMetadata[C, V]
    default_tasks_to_generate: Option[int] = Option[int].maybe(None)

    @abstractmethod
    def generate(self) -> QTask[C, V, Q, A]: ...

    def get_id(self) -> uuid.UUID:
        return self.metadata.id
