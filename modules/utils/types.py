from typing import TypeVar

C = TypeVar("C", default=str)
V = TypeVar("V", default=str)
Q = TypeVar("Q", default=str)
A = TypeVar("A", default=Q | None)
