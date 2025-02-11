from abc import ABC, abstractmethod
from argparse import Namespace
from typing import TypeVar, List, Dict

from data_access.store import DataStore


class CliCommand(ABC):
    def __init__(self, store: DataStore, args):
        self._args = args
        self._store = store

    @classmethod
    @property
    @abstractmethod
    def category(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def arg_specs(cls) -> Dict[str, List]:
        pass

    @abstractmethod
    def handle(self, args: Namespace):
        pass


CommandCategoryType = TypeVar('CommandCategoryType', bound=CliCommand)


