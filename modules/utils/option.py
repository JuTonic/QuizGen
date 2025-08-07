T = TypeVar("T")


def to_option(value: Optional[T]) -> Option[T]:
    return Some()
