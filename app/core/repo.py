from abc import ABC
from typing import Generic, TypeVar


T = TypeVar('T')


class BaseRepo(ABC, Generic[T]):
    pass
