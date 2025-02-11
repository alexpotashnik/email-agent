from argparse import Namespace
from typing import Dict, List

from cli.command import CliCommand


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
