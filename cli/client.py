from argparse import Namespace
from typing import Dict, List

from cli.command import CliCommand


class ClientCommand(CliCommand):
    @classmethod
    @property
    def category(cls) -> str:
        return 'client'

    @classmethod
    def arg_specs(cls) -> Dict[str, List]:
        return {
            'list': [],
            'engage': [
                (['-n', '--name'], {'required': 'true'})
            ]
        }

    def handle(self, args: Namespace):
        match args.command:
            case 'list':
                for c in self._store.list_clients():
                    print(c)

            case 'engage':
                print(self._store.create_client(args.name))

            case _:
                return False

        return True
