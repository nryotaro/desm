"""Provide classes that represent first class collections."""
import abc
import contextlib
from typing import Callable, Sequence, Generator
from .typevar import T, S


class FirstClassFileContextManagerProvider(metaclass=abc.ABCMeta):
    """Provide a context manager."""

    def __init__(self, filename: str):
        """
        """
        self.filename = filename

    @contextlib.contextmanager
    def __call__(self):
        """
        """
        with open(self.filename) as stream:
            yield (self.transform(item.strip()) for item in stream)

    @abc.abstractmethod
    def transform(self, item):
        """
        """


class FirstClassSequence(metaclass=abc.ABCMeta):
    """
    """

    @abc.abstractproperty
    def sequence(self) -> Sequence[T]:
        """
        """

    def __getitem__(self, s):
        """Access the specified items."""
        return self.sequence.__getitem__(s)

    def __len__(self):
        """Return the size of :py:meth:`sequence`."""
        return len(self.sequence)

    def filter_by(self, filter_function: Callable[[T], bool]):
        """Return the sequence that meet `filter_function`."""
        return self.__class__(
            [item for item in self.sequence if filter_function(item)])

    def is_empty(self) -> bool:
        """Return `True` if :py:meth:`sequence` is empty."""
        return len(self.sequence) == 0

    def apply_function(self, function: Callable[[T], S]) \
            -> Generator[S, None, None]:
        """
        """
        return (function(item) for item in self.sequence)
