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


class EnvironmentCommand(CliCommand):
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


class DealsCommand(CliCommand):
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
                self._store.list_deals()

            case _:
                return False

        return True


class ClientCommand(CliCommand):
    @classmethod
    @property
    def category(cls) -> str:
        return 'client'

    @classmethod
    def arg_specs(cls) -> Dict[str, List]:
        return {
            'list': [],
            'engage': [],
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'list':
                for c in self._store.list_clients():
                    print(c)

            case 'engage':
                client = self._store.create_client(f'Client {len(self._store.list_clients())}')
                print(f'{client['id']}: {client['name']}')

            case _:
                return False

        return True


