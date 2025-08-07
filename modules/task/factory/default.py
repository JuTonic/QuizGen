from typing import Callable, override

from modules.tag import Tags
from modules.task import QTask
from modules.task.factory import QTaskFactory
from modules.utils.types import A, C, Q, V


class QTaskFactoryDefault(QTaskFactory[C, V, Q, A]):
    _generator: Callable[[], QTask[C, V, Q, A]]

    def __init__(self, generator: Callable[[], QTask[C, V, Q, A]]):
        self._generator = generator

    @override
    def generate(self) -> QTask[C, V, Q, A]:
        return self._generator()


def task_generator_function():
    alpha = random.randint(1, 9)
    beta = random.randint(1, 9)

    question = f"Чему равна дисперсия величины V({alpha} * X + {beta} * Y), если X и Y подчинены стандартному нормальному закону распределения и независимы друг от друга?"
    answer = f"{alpha ** 2 + beta ** 2}"
    tags = Tags(("тема", "дисперсия"), ("сложность", "лёгкая"))

    return QTask(question, answer, tags)


factory = QTaskFactoryDefault(task_generator_function)
