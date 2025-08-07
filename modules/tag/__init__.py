from collections.abc import Iterable
from dataclasses import dataclass, field
from enum import Enum
from itertools import chain
from typing import Generic, overload, override

from modules.utils.types import C, V


@dataclass(frozen=True)
class Tag(Generic[C, V]):
    """
    Represents a single tag composed of a category and a value

    Attributes:
        cat (C): The category of the tag
        val (V): The value of the tag
    """

    cat: C
    val: V


class Tags(Generic[C, V]):
    """A collection of tags grouped by category

    Attributes:
        _dict: (dict[C, set[V]]): Internal dictionary storing tags grouped by category.
    """

    _dict: dict[C, set[V]]

    @overload
    def __init__(
        self, iter: Iterable[Tag[C, V] | tuple[C, V]] | None = None
    ) -> None: ...

    @overload
    def __init__(
        self,
        iter: Tag[C, V] | tuple[C, V] | None = None,
        **kwargs: Tag[C, V] | tuple[C, V],
    ) -> None: ...

    def __init__(
        self,
        iter: Iterable[Tag[C, V] | tuple[C, V]] | Tag[C, V] | tuple[C, V] | None = None,
        **kwargs: Tag[C, V] | tuple[C, V],
    ) -> None:
        self._dict = {}

        if isinstance(iter, Iterable) and not isinstance(iter, tuple):
            for tag in iter:
                if isinstance(tag, Tag):
                    self._dict.setdefault(tag.cat, set()).add(tag.val)
                else:
                    self._dict.setdefault(tag[0], set()).add(tag[1])
        else:
            for tag in chain([iter], kwargs.values()):
                if isinstance(iter, Tag):
                    self._dict.setdefault(tag.cat, set()).add(tag.val)
                elif isinstance(iter, tuple):
                    self._dict.setdefault(tag[0], set()).add(tag[1])

    @overload
    def has_tag(self, category: C, value: V) -> bool: ...

    @overload
    def has_tag(self, category: Tag[C, V]) -> bool: ...

    def has_tag(self, category: C | Tag[C, V], value: V | None = None) -> bool:
        """Check if a tag exists in the collection.

        Args:
            category (C | Tag[C, V]): The category or a full Tag instance.
            value (V): The value to check (if category is not a Tag).

        Returns:
            bool: True if the tag exists, False otherwise

        Raises:
            AssertionError: If value is None and category is not a Tag.
        """
        if isinstance(category, Tag):
            tag = category
            return tag.val in self._dict.get(tag.cat, set())
        else:
            assert (
                value is not None
            ), "Value must be provided if category is not a tuple"
            return value in self._dict.get(category, set())

    @overload
    def add_tag(self, category: C, value: V) -> None: ...

    @overload
    def add_tag(self, category: Tag[C, V]) -> None: ...

    def add_tag(self, category: C | Tag[C, V], value: V | None = None) -> None:
        """Add a tag to the collection.

        Args:
            category (C | Tag[C, V]): The category or full Tag instance.
            value (V | None): The value to add (if category is not a Tag).

        Raises:
            AssertionError: If value is None and category is not a Tag.
        """
        if isinstance(category, Tag):
            tag = category
            self._dict.get(tag.cat, set()).add(tag.val)
        else:
            assert (
                value is not None
            ), "Value must be provided if category is not a tuple"
            self._dict.get(category, set()).add(value)

    @override
    def __str__(self) -> str:
        """Return a human-readable string representation of the tags.

        Returns:
            str: A formatted string listing categories and their values.
        """
        if len(self._dict) == 0:
            return "No tags"

        lines: list[str] = []
        for category, values in self._dict.items():
            cat_str = str(category.value if isinstance(category, Enum) else category)
            val_strs = [str(v.value if isinstance(v, Enum) else v) for v in values]
            lines.append(f"{cat_str}: {', '.join(val_strs)}")
        return "\n".join(lines)

    def __iter__(self):
        """Yield all tags in the collection one by one.

        Yields:
            Tag[C, V]: Each tag in the collection.
        """

        for category, values in self._dict.items():
            for value in values:
                yield Tag(category, value)
