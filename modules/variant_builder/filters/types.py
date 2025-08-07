from typing import Union

from modules.task import QTask
from modules.task.factory import QTaskFactory

type QTaskOrFactory[C, V, Q, A] = QTask[C, V, Q, A] | QTaskFactory[C, V, Q, A]
