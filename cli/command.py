from abc import ABC, abstractmethod
from argparse import Namespace
from typing import TypeVar, List, Dict

from data_access.store import DataStore


class CommandCategory(ABC):
    def __init__(self, store: DataStore, args):
        self._args = args
        self._store = store

    @classmethod
    @property
    def category(cls) -> str:
        pass

    @abstractmethod
    def handle(self, args: Namespace):
        pass


CommandCategoryType = TypeVar('CommandCategoryType', bound=CommandCategory)


class EnvironmentCommand(CommandCategory):
    @classmethod
    @property
    def category(cls):
        return 'environment'

    @classmethod
    def arg_specs(cls) -> Dict[str, List]:
        return {
            'reset': []
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'reset':
                self._store.clear()

            case _:
                return False

        return True


class DealsCommand(CommandCategory):
    @classmethod
    @property
    def category(cls):
        return 'deals'

    @classmethod
    def arg_specs(cls) -> Dict[str, List]:
        return {
            'list': []
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'list':
                self._store.clear()

            case _:
                return False

        return True
