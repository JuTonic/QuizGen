import random
from dataclasses import dataclass, field
from typing import Generic

from modules.task import QTask
from modules.utils.types import A, C, Q, V


class QTaskPool(list[QTask[C, V, Q, A]], Generic[C, V, Q, A]):
    def shuffle(self):
        random.shuffle(self)
