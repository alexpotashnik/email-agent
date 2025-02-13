from abc import ABC, abstractmethod
from argparse import Namespace
from typing import TypeVar, List, Dict

from agent.email_agent import EmailAgent
from data_access.store import DataStore


class CliCommand(ABC):
    def __init__(self, store: DataStore, email_agent: EmailAgent, args):
        self._store = store
        self._email_agent = email_agent
        self._args = args

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


