from random import Random
from typing import TypeVar


def indent(text: str, spaces: int = 2) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line for line in text.splitlines())


rnd = Random()
rnd.seed(42)
