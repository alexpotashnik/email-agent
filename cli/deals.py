from argparse import Namespace
from typing import Dict, List

from cli.command import CliCommand


class DealsCommand(CliCommand):
    @classmethod
    @property
    def category(cls):
        return 'deals'

    @classmethod
    def arg_specs(cls) -> Dict[str, List]:
        return {
            'list': [],
            'explore': [],
            'negotiate': [],
            'close': []
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'list':
                self._store.list_deals()

            case 'explore':
                raise Exception

            case 'negotiate':
                raise Exception

            case 'close':
                raise Exception

            case _:
                return False

        return True
