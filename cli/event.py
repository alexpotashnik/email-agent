from argparse import Namespace
from typing import Dict, List

from cli.command import CliCommand


class EventCommand(CliCommand):
    @classmethod
    @property
    def category(cls):
        return 'event'

    @classmethod
    def arg_specs(cls) -> Dict[str, List]:
        return {
            'list': []
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'list':
                for e in self._store.list_events():
                    print(e)

            case _:
                return False

        return True
