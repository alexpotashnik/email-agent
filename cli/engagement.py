from argparse import Namespace
from typing import Dict, List

from cli.command import CliCommand


class EngagementCommand(CliCommand):
    @classmethod
    @property
    def category(cls):
        return 'engagement'

    @classmethod
    def arg_specs(cls) -> Dict[str, List]:
        return {
            'list': [],
            'advance': [],
            'close': []
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'list':
                for e in self._store.list_engagements():
                    print(e)

            case 'advance':
                raise Exception

            case 'advance':
                raise Exception

            case _:
                return False

        return True
